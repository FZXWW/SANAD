from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier


ROOT = Path(__file__).resolve().parent
DATASETS_DIR = ROOT / "datasets"


@dataclass
class TrainedAI:
    name: str
    pipeline: Pipeline
    label_encoder: LabelEncoder
    results: pd.DataFrame
    features: list[str]


def build_preprocessor(num_cols: list[str], cat_cols: list[str]) -> ColumnTransformer:
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, num_cols),
            ("cat", categorical_transformer, cat_cols),
        ]
    )


def train_models(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: np.ndarray,
    y_test: np.ndarray,
    preprocessor: ColumnTransformer,
    models: dict[str, Any],
) -> tuple[str, Pipeline, pd.DataFrame]:
    results = []
    fitted_models = {}

    for name, clf in models.items():
        pipe = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", clf),
            ]
        )

        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)
        rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)
        f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)

        fitted_models[name] = pipe
        results.append([name, acc, prec, rec, f1])

    results_df = pd.DataFrame(
        results,
        columns=["Model", "Accuracy", "Precision", "Recall", "F1 Score"],
    ).sort_values(by="F1 Score", ascending=False)

    best_name = results_df.iloc[0]["Model"]
    return best_name, fitted_models[best_name], results_df.reset_index(drop=True)


def user_profile_models() -> dict[str, Any]:
    return {
        "Logistic Regression": LogisticRegression(C=0.5, solver="saga", max_iter=5000),
        "Decision Tree": DecisionTreeClassifier(
            max_depth=12,
            min_samples_leaf=10,
            criterion="entropy",
            random_state=42,
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=300,
            max_depth=8,
            max_features="sqrt",
            bootstrap=True,
            random_state=42,
        ),
        "Gradient Boosting": GradientBoostingClassifier(
            n_estimators=150,
            learning_rate=0.05,
            subsample=0.8,
            max_depth=4,
            random_state=42,
        ),
        "MLP (Deep Learning)": MLPClassifier(
            hidden_layer_sizes=(100, 100),
            alpha=0.1,
            solver="adam",
            max_iter=1000,
            random_state=42,
        ),
    }


def stock_models() -> dict[str, Any]:
    return {
        "Logistic Regression": LogisticRegression(C=1, solver="lbfgs", max_iter=3000),
        "Decision Tree": DecisionTreeClassifier(max_depth=5, min_samples_split=5, min_samples_leaf=2),
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=10, min_samples_split=5),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=200, learning_rate=0.01, max_depth=5),
        "MLP (Deep Learning)": MLPClassifier(
            hidden_layer_sizes=(256, 128),
            alpha=0.01,
            learning_rate_init=0.01,
            max_iter=500,
        ),
    }


def fund_models() -> dict[str, Any]:
    return {
        "Logistic Regression": LogisticRegression(C=0.5, solver="saga", max_iter=5000),
        "Decision Tree": DecisionTreeClassifier(max_depth=12, min_samples_leaf=10, criterion="entropy"),
        "Random Forest": RandomForestClassifier(
            n_estimators=300,
            max_depth=8,
            max_features="sqrt",
            bootstrap=True,
        ),
        "Gradient Boosting": GradientBoostingClassifier(
            n_estimators=150,
            learning_rate=0.05,
            subsample=0.8,
            max_depth=4,
        ),
        "MLP (Deep Learning)": MLPClassifier(
            hidden_layer_sizes=(100, 100),
            alpha=0.1,
            solver="adam",
            max_iter=1000,
        ),
    }


def train_user_profile_ai() -> TrainedAI:
    df = pd.read_csv(DATASETS_DIR / "user_profiles.csv")

    features = [
        "age",
        "monthly_income",
        "investment_capital",
        "investment_horizon",
        "risk_tolerance",
        "investment_goal",
        "preferred_market",
        "experience_level",
        "liquidity_need",
    ]

    cat_cols = [
        "investment_horizon",
        "risk_tolerance",
        "investment_goal",
        "preferred_market",
        "experience_level",
        "liquidity_need",
    ]
    num_cols = ["age", "monthly_income", "investment_capital"]

    X = df[features]
    y = df["recommended_market"]

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y_encoded,
        test_size=0.20,
        random_state=42,
        stratify=y_encoded,
    )

    preprocessor = build_preprocessor(num_cols, cat_cols)
    best_name, best_pipeline, results = train_models(
        X_train,
        X_test,
        y_train,
        y_test,
        preprocessor,
        user_profile_models(),
    )

    return TrainedAI(best_name, best_pipeline, le, results, features)


def read_saudi_stock_files() -> pd.DataFrame:
    files_map = {
        "SA_Stock_ACWA.csv": ("Utilities", "Electric Utilities"),
        "SA_Stock_AlRajhi.csv": ("Financials", "Banks"),
        "SA_Stock_Aramco.csv": ("Energy", "Oil & Gas"),
        "SA_Stock_Maaden.csv": ("Materials", "Mining"),
        "SA_Stock_SABIC.csv": ("Materials", "Chemicals"),
        "SA_Stock_SNB.csv": ("Financials", "Banks"),
        "SA_Stock_STC.csv": ("Communication Services", "Telecom"),
    }

    all_df = []
    for file_name, (sector, industry) in files_map.items():
        df = pd.read_csv(DATASETS_DIR / file_name, header=None, skiprows=3)
        df.columns = ["Date", "Close", "High", "Low", "Open", "Volume", "Ticker", "Company_Name"]
        df["Sector"] = sector
        df["Industry"] = industry
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        numeric_cols = ["Close", "High", "Low", "Open", "Volume"]
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
        all_df.append(df)

    df_saudi = pd.concat(all_df, ignore_index=True)
    df_saudi = df_saudi.sort_values(by=["Ticker", "Date"]).dropna(subset=["Date", "Close"])
    return df_saudi


def prepare_saudi_stock_ai_data() -> pd.DataFrame:
    df_saudi = read_saudi_stock_files()
    df_saudi["Adj_Close"] = df_saudi["Close"]
    df_saudi["Future_Close"] = df_saudi.groupby("Ticker")["Close"].shift(-7)
    df_saudi["Future_Return"] = (df_saudi["Future_Close"] - df_saudi["Close"]) / df_saudi["Close"]
    df_saudi = df_saudi.dropna(subset=["Future_Return"])

    df_saudi["Ticker"] = df_saudi["Company_Name"]
    best_stocks = df_saudi.loc[df_saudi.groupby("Date")["Future_Return"].idxmax()]
    best_stocks = best_stocks[["Date", "Company_Name"]].rename(columns={"Company_Name": "Target"})

    if "Target" in df_saudi.columns:
        df_saudi = df_saudi.drop(columns=["Target"])

    df_saudi = df_saudi.merge(best_stocks, on="Date")
    return df_saudi.sort_values(by=["Ticker", "Date"]).reset_index(drop=True)


def train_saudi_stock_ai() -> tuple[TrainedAI, pd.DataFrame]:
    df_saudi = prepare_saudi_stock_ai_data()

    features = ["Ticker", "Sector", "Industry", "Open", "High", "Low", "Close", "Adj_Close", "Volume"]
    cat_cols = ["Ticker", "Sector", "Industry"]
    num_cols = ["Open", "High", "Low", "Close", "Adj_Close", "Volume"]

    split_date = pd.to_datetime("2024-01-01")
    le = LabelEncoder()
    le.fit(df_saudi["Target"])

    train_data = df_saudi[df_saudi["Date"] < split_date]
    test_data = df_saudi[df_saudi["Date"] >= split_date]

    X_train = train_data[features]
    X_test = test_data[features]
    y_train = le.transform(train_data["Target"])
    y_test = le.transform(test_data["Target"])

    preprocessor = build_preprocessor(num_cols, cat_cols)
    best_name, best_pipeline, results = train_models(
        X_train,
        X_test,
        y_train,
        y_test,
        preprocessor,
        stock_models(),
    )

    return TrainedAI(best_name, best_pipeline, le, results, features), df_saudi


def compute_rsi(series: pd.Series, window: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(window).mean()
    loss = (-delta.clip(upper=0)).rolling(window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def prepare_fund_ai_data() -> pd.DataFrame:
    df = pd.read_csv(ROOT / "SA_Investment_Funds" / "sa_fund_prices_daily.csv")

    funds = [
        "iShares MSCI Saudi KSA",
        "Franklin FTSE Saudi ETF",
        "TASI Index",
    ]
    df = df[df["Company_Name"].isin(funds)].copy()

    numeric_cols = ["Open", "High", "Low", "Close", "Adj_Close", "Volume"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])
    df = df.sort_values(["Ticker", "Date"]).reset_index(drop=True)

    df["Daily_Return"] = df.groupby("Ticker")["Close"].pct_change()
    df["MA_5"] = df.groupby("Ticker")["Close"].transform(lambda x: x.rolling(5).mean())
    df["MA_10"] = df.groupby("Ticker")["Close"].transform(lambda x: x.rolling(10).mean())
    df["MA_20"] = df.groupby("Ticker")["Close"].transform(lambda x: x.rolling(20).mean())
    df["MA_ratio"] = df["MA_5"] / df["MA_20"]
    df["Volatility_7"] = df.groupby("Ticker")["Daily_Return"].transform(lambda x: x.rolling(7).std())
    df["Momentum_10"] = df.groupby("Ticker")["Close"].transform(lambda x: x.pct_change(10))
    df["Price_Range"] = (df["High"] - df["Low"]) / df["Close"]
    df["Volume_MA_5"] = df.groupby("Ticker")["Volume"].transform(lambda x: x.rolling(5).mean())
    df["Volume_ratio"] = df["Volume"] / df["Volume_MA_5"]
    df["RSI_14"] = df.groupby("Ticker")["Close"].transform(compute_rsi)

    df["Future_Return"] = df.groupby("Ticker")["Close"].transform(lambda x: x.shift(-7).sub(x).div(x))
    df["Target"] = pd.qcut(df["Future_Return"], q=3, labels=["Weak", "Neutral", "Strong"])
    df = df.dropna().reset_index(drop=True)
    return df


def train_fund_ai() -> tuple[TrainedAI, pd.DataFrame]:
    df = prepare_fund_ai_data()

    features = [
        "Ticker",
        "MA_5",
        "MA_10",
        "MA_20",
        "MA_ratio",
        "RSI_14",
        "Volatility_7",
        "Momentum_10",
        "Price_Range",
        "Volume_ratio",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
    ]
    cat_cols = ["Ticker"]
    num_cols = [
        "MA_5",
        "MA_10",
        "MA_20",
        "MA_ratio",
        "RSI_14",
        "Volatility_7",
        "Momentum_10",
        "Price_Range",
        "Volume_ratio",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
    ]

    split_date = "2024-01-01"
    le = LabelEncoder()
    le.fit(df["Target"])

    train = df[df["Date"] < split_date]
    test = df[df["Date"] >= split_date]

    X_train = train[features]
    X_test = test[features]
    y_train = le.transform(train["Target"])
    y_test = le.transform(test["Target"])

    preprocessor = build_preprocessor(num_cols, cat_cols)
    best_name, best_pipeline, results = train_models(
        X_train,
        X_test,
        y_train,
        y_test,
        preprocessor,
        fund_models(),
    )

    return TrainedAI(best_name, best_pipeline, le, results, features), df


def prepare_us_stock_ai_data() -> pd.DataFrame:
    df = pd.read_csv(DATASETS_DIR / "US_Stock_Market.csv")

    companies = [
        "Microsoft Corporation",
        "Apple Inc.",
        "NVIDIA Corporation",
        "Alphabet Inc.",
        "Amazon.com, Inc.",
        "Meta Platforms, Inc.",
        "Berkshire Hathaway Inc.",
    ]

    df = df[df["Company_Name"].isin(companies)].copy()
    numeric_cols = ["Open", "High", "Low", "Close", "Adj_Close", "Volume"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
    df["Date"] = pd.to_datetime(df["Date"], utc=True, errors="coerce")
    df["Date"] = df["Date"].dt.tz_localize(None)
    df = df.sort_values(by=["Ticker", "Date"])

    df["Future_Close"] = df.groupby("Ticker")["Close"].shift(-7)
    df["Future_Return"] = (df["Future_Close"] - df["Close"]) / df["Close"]
    df = df.dropna(subset=["Future_Close", "Future_Return"])

    best_company = df.loc[df.groupby("Date")["Future_Return"].idxmax()]
    best_company = best_company[["Date", "Ticker"]].rename(columns={"Ticker": "Target"})
    df = df.merge(best_company, on="Date")
    return df


def train_us_stock_ai() -> tuple[TrainedAI, pd.DataFrame]:
    df = prepare_us_stock_ai_data()

    features = ["Ticker", "Sector", "Industry", "Open", "High", "Low", "Close", "Adj_Close", "Volume"]
    cat_cols = ["Ticker", "Sector", "Industry"]
    num_cols = ["Open", "High", "Low", "Close", "Adj_Close", "Volume"]

    split_date = "2024-01-01"
    le = LabelEncoder()
    le.fit(df["Target"])

    train = df[df["Date"] < split_date]
    test = df[df["Date"] >= split_date]

    X_train = train[features]
    X_test = test[features]
    y_train = le.transform(train["Target"])
    y_test = le.transform(test["Target"])

    preprocessor = build_preprocessor(num_cols, cat_cols)
    best_name, best_pipeline, results = train_models(
        X_train,
        X_test,
        y_train,
        y_test,
        preprocessor,
        stock_models(),
    )

    return TrainedAI(best_name, best_pipeline, le, results, features), df


def preferred_tenor_months(investment_horizon: str) -> int:
    if investment_horizon == "short":
        return 3
    if investment_horizon == "medium":
        return 12
    return 24


def recommend_deposit_product(user_profile: dict[str, Any], top_n: int = 5) -> pd.DataFrame:
    deposits_df = pd.read_csv(DATASETS_DIR / "SA_Deposit_Products.csv")

    numeric_deposit_cols = ["min_amount_sar", "max_amount_sar", "tenor_months", "annual_return_pct"]
    for col in numeric_deposit_cols:
        deposits_df[col] = pd.to_numeric(deposits_df[col], errors="coerce")

    capital = user_profile["investment_capital"]
    target_tenor = preferred_tenor_months(user_profile["investment_horizon"])
    liquidity_need = user_profile["liquidity_need"]

    candidates = deposits_df.copy()
    candidates["min_amount_sar"] = candidates["min_amount_sar"].fillna(0)
    candidates["max_amount_sar"] = candidates["max_amount_sar"].fillna(np.inf)
    candidates["annual_return_pct"] = candidates["annual_return_pct"].fillna(0)

    candidates = candidates[
        (capital >= candidates["min_amount_sar"])
        & (capital <= candidates["max_amount_sar"])
    ].copy()

    if candidates.empty:
        return pd.DataFrame()

    liquidity_score_map = {"high": 3, "medium": 2, "low": 1}
    user_liq_score = liquidity_score_map.get(liquidity_need, 2)
    candidates["product_liq_score"] = candidates["liquidity_level"].map(liquidity_score_map).fillna(2)

    candidates["tenor_fit_score"] = 1 / (1 + (candidates["tenor_months"] - target_tenor).abs())
    candidates["liquidity_fit_score"] = 1 / (1 + (candidates["product_liq_score"] - user_liq_score).abs())
    max_return = candidates["annual_return_pct"].max()
    candidates["return_score"] = np.where(max_return > 0, candidates["annual_return_pct"] / max_return, 0)

    candidates["deposit_match_score"] = (
        0.45 * candidates["tenor_fit_score"]
        + 0.35 * candidates["liquidity_fit_score"]
        + 0.20 * candidates["return_score"]
    )

    result_cols = [
        "bank",
        "product_name",
        "product_type",
        "min_amount_sar",
        "max_amount_sar",
        "tenor_months",
        "liquidity_level",
        "annual_return_pct",
        "rate_type",
        "deposit_match_score",
        "source_url",
    ]

    return candidates.sort_values("deposit_match_score", ascending=False)[result_cols].head(top_n)


def latest_rows_for_prediction(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    return df.sort_values("Date").groupby(group_col).tail(1).copy()


def predict_ranked_assets(ai: TrainedAI, latest_rows: pd.DataFrame, name_col: str | None = None) -> pd.DataFrame:
    X_latest = latest_rows[ai.features]
    pred_encoded = ai.pipeline.predict(X_latest)
    pred_labels = ai.label_encoder.inverse_transform(pred_encoded)

    output = latest_rows.copy()
    output["AI_Prediction"] = pred_labels

    if hasattr(ai.pipeline.named_steps["model"], "predict_proba"):
        probabilities = ai.pipeline.predict_proba(X_latest)
        output["AI_Confidence"] = probabilities.max(axis=1)
    else:
        output["AI_Confidence"] = np.nan

    cols = ["Date", "Ticker"]
    if name_col and name_col in output.columns:
        cols.append(name_col)
    cols += ["AI_Prediction", "AI_Confidence", "Close", "Volume"]
    return output[cols].sort_values("AI_Confidence", ascending=False)


def recommend_saudi_stocks_with_ai(ai: TrainedAI, df_saudi: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    latest = latest_rows_for_prediction(df_saudi, "Ticker")
    ranked = predict_ranked_assets(ai, latest, "Company_Name")
    return ranked[ranked["AI_Prediction"].eq(ranked["Company_Name"])].head(top_n)


def recommend_funds_with_ai(ai: TrainedAI, df_funds: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    latest = latest_rows_for_prediction(df_funds, "Ticker")
    ranked = predict_ranked_assets(ai, latest, "Company_Name")
    strong = ranked[ranked["AI_Prediction"].eq("Strong")]
    if strong.empty:
        return ranked.head(top_n)
    return strong.head(top_n)


def recommend_us_stocks_with_ai(ai: TrainedAI, df_us: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    latest = latest_rows_for_prediction(df_us, "Ticker")
    ranked = predict_ranked_assets(ai, latest, "Company_Name")
    return ranked[ranked["AI_Prediction"].eq(ranked["Ticker"])].head(top_n)


class SanadAIFullSystem:
    def __init__(self) -> None:
        self.user_ai: TrainedAI | None = None
        self.saudi_stock_ai: TrainedAI | None = None
        self.fund_ai: TrainedAI | None = None
        self.us_stock_ai: TrainedAI | None = None

        self.saudi_stock_data: pd.DataFrame | None = None
        self.fund_data: pd.DataFrame | None = None
        self.us_stock_data: pd.DataFrame | None = None

    def train_all(self) -> None:
        self.user_ai = train_user_profile_ai()
        self.saudi_stock_ai, self.saudi_stock_data = train_saudi_stock_ai()
        self.fund_ai, self.fund_data = train_fund_ai()
        self.us_stock_ai, self.us_stock_data = train_us_stock_ai()

    def model_results(self) -> dict[str, pd.DataFrame]:
        return {
            "User_Profile_AI": self.user_ai.results,
            "Saudi_Stock_AI": self.saudi_stock_ai.results,
            "Saudi_Fund_AI": self.fund_ai.results,
            "US_Stock_AI": self.us_stock_ai.results,
        }

    def predict_category(self, user_profile: dict[str, Any]) -> tuple[str, float]:
        X_user = pd.DataFrame([user_profile])[self.user_ai.features]
        pred_encoded = self.user_ai.pipeline.predict(X_user)
        category = self.user_ai.label_encoder.inverse_transform(pred_encoded)[0]

        confidence = np.nan
        if hasattr(self.user_ai.pipeline.named_steps["model"], "predict_proba"):
            confidence = float(self.user_ai.pipeline.predict_proba(X_user).max(axis=1)[0])

        return category, confidence

    def recommend(self, user_profile: dict[str, Any], top_n: int = 5) -> dict[str, Any]:
        category, confidence = self.predict_category(user_profile)

        if category == "Deposits":
            final_recommendations = recommend_deposit_product(user_profile, top_n)
        elif category == "Saudi_Stocks":
            final_recommendations = recommend_saudi_stocks_with_ai(
                self.saudi_stock_ai,
                self.saudi_stock_data,
                top_n,
            )
        elif category == "Saudi_Funds":
            final_recommendations = recommend_funds_with_ai(
                self.fund_ai,
                self.fund_data,
                top_n,
            )
        elif category == "US_Stocks":
            final_recommendations = recommend_us_stocks_with_ai(
                self.us_stock_ai,
                self.us_stock_data,
                top_n,
            )
        elif category == "Mixed":
            parts = [
                recommend_deposit_product(user_profile, 1).assign(Category="Deposits"),
                recommend_funds_with_ai(self.fund_ai, self.fund_data, 1).assign(Category="Saudi_Funds"),
                recommend_saudi_stocks_with_ai(self.saudi_stock_ai, self.saudi_stock_data, 1).assign(Category="Saudi_Stocks"),
                recommend_us_stocks_with_ai(self.us_stock_ai, self.us_stock_data, 1).assign(Category="US_Stocks"),
            ]
            final_recommendations = pd.concat(parts, ignore_index=True, sort=False)
        else:
            final_recommendations = pd.DataFrame()

        return {
            "recommended_category": category,
            "category_confidence": confidence,
            "final_recommendations": final_recommendations,
        }


def sample_user(user_id: str = "USR0004") -> dict[str, Any]:
    users = pd.read_csv(DATASETS_DIR / "user_profiles.csv")
    row = users.loc[users["user_id"] == user_id].iloc[0]
    fields = [
        "age",
        "monthly_income",
        "investment_capital",
        "investment_horizon",
        "risk_tolerance",
        "investment_goal",
        "preferred_market",
        "experience_level",
        "liquidity_need",
    ]
    return row[fields].to_dict()


if __name__ == "__main__":
    system = SanadAIFullSystem()
    system.train_all()

    user = sample_user("USR0004")
    result = system.recommend(user, top_n=5)

    print("Recommended Category:", result["recommended_category"])
    print("Category Confidence:", result["category_confidence"])
    print()
    print(result["final_recommendations"].to_string(index=False))
