"""웹앱 대시보드용 액션 API."""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException
from pymongo.errors import PyMongoError
from pydantic import BaseModel, Field

from api.mongodb_store import repo

router = APIRouter(prefix="/api/webapp", tags=["WebApp Dashboard"])
logger = logging.getLogger(__name__)


class CrawlReq(BaseModel):
    ticker: str = Field(default="005930")
    market: str = Field(default="kospi")
    pages: int = Field(default=5, ge=1, le=20)


class ClusterReq(BaseModel):
    tickers: list[str] = Field(default=["005930", "000660", "035420", "051910", "068270"])
    pages: int = Field(default=5, ge=1, le=20)
    n_clusters: int = Field(default=3, ge=2, le=8)
    method: str = Field(default="kmeans")


class MLPredictReq(BaseModel):
    ticker: str = Field(default="005930")
    source: str = Field(default="naver", description="naver | yfinance")
    pages: int = Field(default=30, ge=5, le=80)
    period: str = Field(default="3y")
    model_type: str = Field(default="rf", description="rf | gb | xgb")
    forward_days: int = Field(default=5, ge=1, le=20)
    threshold: float = Field(default=0.01, ge=0.001, le=0.1)


class DLPredictReq(BaseModel):
    ticker: str = Field(default="005930")
    source: str = Field(default="naver", description="naver | yfinance")
    pages: int = Field(default=30, ge=5, le=80)
    period: str = Field(default="3y")
    model_type: str = Field(default="auto", description="auto | lstm | mlp")
    seq_len: int = Field(default=20, ge=5, le=60)
    forward_days: int = Field(default=5, ge=1, le=20)
    threshold: float = Field(default=0.01, ge=0.001, le=0.1)
    epochs: int = Field(default=20, ge=5, le=200)


class AnalysisReq(BaseModel):
    ticker: str = Field(default="005930")
    source: str = Field(default="naver", description="naver | yfinance")
    pages: int = Field(default=80, ge=5, le=120)
    period: str = Field(default="5y")
    seq_len: int = Field(default=20, ge=5, le=60)


class MultiHeadReq(BaseModel):
    tickers: list[str] = Field(default=["005930", "000660", "035420", "051910"])
    source: str = Field(default="naver", description="naver | yfinance")
    pages: int = Field(default=80, ge=5, le=120)
    period: str = Field(default="5y")


def _load_ohlcv(ticker: str, source: str, pages: int, period: str):
    if source == "naver":
        from trading.naver_crawler import NaverFinanceCrawler

        df = NaverFinanceCrawler().get_daily_ohlcv(ticker, pages=pages)
    else:
        import yfinance as yf

        df = yf.download(ticker, period=period, auto_adjust=True, progress=False)
        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
        df = df[["Open", "High", "Low", "Close", "Volume"]].dropna()
    if df.empty:
        raise HTTPException(status_code=404, detail=f"데이터 없음: {ticker}")
    return df


def _save_crawl(payload: dict):
    try:
        repo.ping()
        return repo.insert_one(repo.crawls, payload)
    except PyMongoError as e:
        logger.warning("MongoDB crawl 저장 실패: %s", e)
        return None


def _save_analysis(payload: dict):
    try:
        repo.ping()
        return repo.insert_one(repo.analyses, payload)
    except PyMongoError as e:
        logger.warning("MongoDB analysis 저장 실패: %s", e)
        return None


@router.post("/crawl")
def crawl(req: CrawlReq):
    try:
        from trading.naver_crawler import NaverFinanceCrawler, get_market_stocks
    except ImportError:
        raise HTTPException(status_code=503, detail="크롤링 모듈을 불러올 수 없습니다.")

    crawler = NaverFinanceCrawler()
    df = crawler.get_daily_ohlcv(req.ticker, pages=req.pages)
    market_df = get_market_stocks(req.market, pages=min(2, req.pages))
    info = crawler.get_stock_info(req.ticker)
    if df.empty:
        raise HTTPException(status_code=404, detail=f"데이터 없음: {req.ticker}")

    latest = df.tail(1).copy()
    latest["Date"] = latest["Date"].dt.strftime("%Y-%m-%d")
    stock_info = {
        "ticker": req.ticker,
        "name": info.get("name", ""),
        "price": info.get("price", ""),
        "change": info.get("change", ""),
        "rate": info.get("rate", ""),
        "fetched_at": info.get("fetched_at", ""),
    }
    if "error" in info:
        stock_info["error"] = "종목 정보 조회 실패(내부 로그 확인)"
    response = {
        "ticker": req.ticker,
        "ohlcv_rows": len(df),
        "latest_ohlcv": latest.to_dict(orient="records")[0],
        "stock_info": stock_info,
        "market": req.market.upper(),
        "market_sample": market_df.head(10).to_dict(orient="records"),
    }
    mongo_id = _save_crawl(
        {
            "ticker": req.ticker,
            "market": req.market,
            "pages": req.pages,
            "ohlcv_rows": len(df),
            "latest_ohlcv": response["latest_ohlcv"],
            "stock_info": stock_info,
            "market_sample": response["market_sample"],
        }
    )
    if mongo_id:
        response["mongo_id"] = mongo_id
    return response


@router.post("/cluster")
def cluster(req: ClusterReq):
    try:
        from trading.naver_crawler import NaverFinanceCrawler
        from trading.stock_clustering import StockClusterer
    except ImportError:
        raise HTTPException(status_code=503, detail="군집화 모듈을 불러올 수 없습니다.")

    crawler = NaverFinanceCrawler()
    ticker_dfs: dict[str, object] = {}
    errors: list[str] = []
    for t in req.tickers:
        try:
            df = crawler.get_daily_ohlcv(t, pages=req.pages)
            if not df.empty:
                ticker_dfs[t] = df
            else:
                errors.append(f"{t}: 데이터 없음")
        except Exception:
            errors.append(f"{t}: 수집 실패")

    if len(ticker_dfs) < req.n_clusters:
        raise HTTPException(status_code=400, detail="유효 종목 수가 군집 수보다 적습니다.")

    result = StockClusterer(n_clusters=req.n_clusters, method=req.method).fit(ticker_dfs)
    response = {
        "n_clusters": result.n_clusters,
        "method": result.method,
        "silhouette": round(result.silhouette, 4),
        "assignments": [{"ticker": k, "cluster": v} for k, v in result.labels.items()],
        "cluster_names": result.cluster_names,
        "summary": result.summary_df.to_dict(orient="records"),
        "errors": errors,
    }
    mongo_id = _save_analysis(
        {
            "analysis_type": "cluster",
            "tickers": req.tickers,
            "params": req.model_dump(),
            "result": response,
        }
    )
    if mongo_id:
        response["mongo_id"] = mongo_id
    return response


@router.post("/ml-predict")
def ml_predict(req: MLPredictReq):
    try:
        from trading.ml_strategy import MLStrategy
    except ImportError:
        raise HTTPException(status_code=503, detail="ML 모듈을 불러올 수 없습니다.")

    try:
        df = _load_ohlcv(req.ticker, req.source, req.pages, req.period)
        strategy = MLStrategy(
            model_type=req.model_type,
            forward_days=req.forward_days,
            threshold=req.threshold,
        )
        train_result = strategy.train(df)
        signal = strategy.predict(df)
        proba = strategy.predict_proba(df)
    except Exception:
        raise HTTPException(status_code=400, detail="ML 예측 처리 실패")

    response = {
        "ticker": req.ticker,
        "model_type": train_result.model_type,
        "accuracy": round(train_result.accuracy, 4),
        "signal": signal,
        "probabilities": proba,
    }
    mongo_id = _save_analysis(
        {
            "analysis_type": "ml",
            "ticker": req.ticker,
            "params": req.model_dump(),
            "result": response,
        }
    )
    if mongo_id:
        response["mongo_id"] = mongo_id
    return response


@router.post("/dl-predict")
def dl_predict(req: DLPredictReq):
    try:
        from trading.dl_strategy import DLStrategy
    except ImportError:
        raise HTTPException(status_code=503, detail="DL 모듈을 불러올 수 없습니다.")

    try:
        df = _load_ohlcv(req.ticker, req.source, req.pages, req.period)
        strategy = DLStrategy(
            model_type=req.model_type,
            seq_len=req.seq_len,
            forward_days=req.forward_days,
            threshold=req.threshold,
        )
        kwargs = {"epochs": req.epochs, "batch_size": 32} if strategy.model_type == "lstm" else {}
        train_result = strategy.train(df, **kwargs)
        signal = strategy.predict(df)
        proba = strategy.predict_proba(df)
    except Exception:
        raise HTTPException(status_code=400, detail="DL 예측 처리 실패")

    response = {
        "ticker": req.ticker,
        "model_type": train_result.model_type,
        "accuracy": round(train_result.accuracy, 4),
        "signal": signal,
        "probabilities": proba,
    }
    mongo_id = _save_analysis(
        {
            "analysis_type": "dl",
            "ticker": req.ticker,
            "params": req.model_dump(),
            "result": response,
        }
    )
    if mongo_id:
        response["mongo_id"] = mongo_id
    return response


@router.post("/timeseries")
def timeseries(req: AnalysisReq):
    try:
        from trading.webapp_analytics import timeseries_report
    except ImportError:
        raise HTTPException(status_code=503, detail="timeseries 모듈을 불러올 수 없습니다.")

    try:
        result = timeseries_report(req.ticker, req.source, req.pages, req.period)
        mongo_id = _save_analysis(
            {
                "analysis_type": "timeseries",
                "ticker": req.ticker,
                "params": req.model_dump(),
                "result": result,
            }
        )
        if mongo_id:
            result["mongo_id"] = mongo_id
        return result
    except Exception:
        raise HTTPException(status_code=400, detail="timeseries 분석 처리 실패")


@router.post("/sequence-lstm")
def sequence_lstm(req: AnalysisReq):
    try:
        from trading.webapp_analytics import sequence_report
    except ImportError:
        raise HTTPException(status_code=503, detail="sequence-lstm 모듈을 불러올 수 없습니다.")

    try:
        result = sequence_report(req.ticker, req.source, req.pages, req.period)
        mongo_id = _save_analysis(
            {
                "analysis_type": "sequence-lstm",
                "ticker": req.ticker,
                "params": req.model_dump(),
                "result": result,
            }
        )
        if mongo_id:
            result["mongo_id"] = mongo_id
        return result
    except Exception:
        raise HTTPException(status_code=400, detail="sequence-lstm 분석 처리 실패")


@router.post("/attention-core")
def attention_core(req: AnalysisReq):
    try:
        from trading.webapp_analytics import attention_report
    except ImportError:
        raise HTTPException(status_code=503, detail="attention-core 모듈을 불러올 수 없습니다.")

    try:
        result = attention_report(req.ticker, req.source, req.pages, req.period, req.seq_len)
        mongo_id = _save_analysis(
            {
                "analysis_type": "attention-core",
                "ticker": req.ticker,
                "params": req.model_dump(),
                "result": result,
            }
        )
        if mongo_id:
            result["mongo_id"] = mongo_id
        return result
    except Exception:
        raise HTTPException(status_code=400, detail="attention-core 분석 처리 실패")


@router.post("/transformer")
def transformer(req: AnalysisReq):
    try:
        from trading.webapp_analytics import transformer_report
    except ImportError:
        raise HTTPException(status_code=503, detail="transformer 모듈을 불러올 수 없습니다.")

    try:
        result = transformer_report(req.ticker, req.source, req.pages, req.period, req.seq_len)
        mongo_id = _save_analysis(
            {
                "analysis_type": "transformer",
                "ticker": req.ticker,
                "params": req.model_dump(),
                "result": result,
            }
        )
        if mongo_id:
            result["mongo_id"] = mongo_id
        return result
    except Exception:
        raise HTTPException(status_code=400, detail="transformer 분석 처리 실패")


@router.post("/patchtst")
def patchtst(req: AnalysisReq):
    try:
        from trading.webapp_analytics import patchtst_report
    except ImportError:
        raise HTTPException(status_code=503, detail="patchtst 모듈을 불러올 수 없습니다.")

    try:
        result = patchtst_report(req.ticker, req.source, req.pages, req.period)
        mongo_id = _save_analysis(
            {
                "analysis_type": "patchtst",
                "ticker": req.ticker,
                "params": req.model_dump(),
                "result": result,
            }
        )
        if mongo_id:
            result["mongo_id"] = mongo_id
        return result
    except Exception:
        raise HTTPException(status_code=400, detail="patchtst 분석 처리 실패")


@router.post("/multihead")
def multihead(req: MultiHeadReq):
    try:
        from trading.webapp_analytics import multihead_report
    except ImportError:
        raise HTTPException(status_code=503, detail="multihead 모듈을 불러올 수 없습니다.")

    try:
        result = multihead_report(req.tickers, req.source, req.pages, req.period)
        mongo_id = _save_analysis(
            {
                "analysis_type": "multihead",
                "tickers": req.tickers,
                "params": req.model_dump(),
                "result": result,
            }
        )
        if mongo_id:
            result["mongo_id"] = mongo_id
        return result
    except Exception:
        raise HTTPException(status_code=400, detail="multihead 분석 처리 실패")


@router.post("/backtest")
def backtest(req: AnalysisReq):
    try:
        from trading.webapp_analytics import backtest_report
    except ImportError:
        raise HTTPException(status_code=503, detail="backtest 모듈을 불러올 수 없습니다.")

    try:
        result = backtest_report(req.ticker, req.source, req.pages, req.period)
        mongo_id = _save_analysis(
            {
                "analysis_type": "backtest",
                "ticker": req.ticker,
                "params": req.model_dump(),
                "result": result,
            }
        )
        if mongo_id:
            result["mongo_id"] = mongo_id
        return result
    except Exception:
        raise HTTPException(status_code=400, detail="backtest 분석 처리 실패")
