from pathlib import Path
import re
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "dataset" / "processed" / "cleaned_courses.csv"
OUTPUT_FILE = BASE_DIR / "dataset" / "processed" / "featured_courses.csv"


def convert_students(value):
    if pd.isna(value):
        return 0

    value = str(value).lower().replace(",", "").strip()

    try:
        if value.endswith("k"):
            return float(value[:-1]) * 1000
        if value.endswith("m"):
            return float(value[:-1]) * 1000000
        return float(value)
    except:
        return 0


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def feature_engineering():

    df = pd.read_csv(INPUT_FILE)
    df = df.dropna(subset=["course_title"])
    df = df.reset_index(drop=True)

    df = df.drop_duplicates(subset=["course_title"])
    df = df.reset_index(drop=True)

    df["students_enrolled_numeric"] = (
        df["course_students_enrolled"]
        .apply(convert_students)
    )

    df["course_title"] = df["course_title"].apply(clean_text)
    df["course_organization"] = df["course_organization"].apply(clean_text)
    df["course_Certificate_type"] = df["course_Certificate_type"].apply(clean_text)
    df["course_difficulty"] = df["course_difficulty"].apply(clean_text)

    df["combined_features"] = (
        df["course_title"] + " " +
        df["course_organization"] + " " +
        df["course_Certificate_type"] + " " +
        df["course_difficulty"]
    )

    difficulty_encoder = LabelEncoder()
    certificate_encoder = LabelEncoder()

    df["difficulty_encoded"] = difficulty_encoder.fit_transform(
        df["course_difficulty"]
    )

    df["certificate_encoded"] = certificate_encoder.fit_transform(
        df["course_Certificate_type"]
    )

    df["popularity_score"] = (
        df["course_rating"] * 0.6 +
        np.log1p(df["students_enrolled_numeric"]) * 0.4
    )

    scaler = MinMaxScaler()

    df["popularity_score"] = scaler.fit_transform(
        df[["popularity_score"]]
    )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)

    print("\nFeature Engineering Completed Successfully")
    print(f"Total Courses : {len(df)}")
    print(f"Output File   : {OUTPUT_FILE}")


if __name__ == "__main__":
    feature_engineering()