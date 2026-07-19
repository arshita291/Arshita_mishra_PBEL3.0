from pathlib import Path
import pandas as pd

# -----------------------------
# Project Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA = BASE_DIR / "dataset" / "raw" / "coursera_data.csv"
PROCESSED_DATA = BASE_DIR / "dataset" / "processed" / "cleaned_courses.csv"


def clean_dataset():
    """
    Load, clean and save the Coursera dataset.
    """

    print("Loading dataset...")

    df = pd.read_csv(RAW_DATA)

    print(f"Original Shape : {df.shape}")

    # Remove unwanted index column if present
    if "Unnamed: 0" in df.columns:
        df.drop(columns=["Unnamed: 0"], inplace=True)

    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

    # Remove rows having missing course title
    df.dropna(subset=["course_title"], inplace=True)

    # Fill missing values
    df["course_rating"] = df["course_rating"].fillna(df["course_rating"].median())

    df["course_difficulty"] = df["course_difficulty"].fillna("Unknown")

    df["course_Certificate_type"] = df["course_Certificate_type"].fillna("Unknown")

    df["course_organization"] = df["course_organization"].fillna("Unknown")

    # Clean text columns
    text_columns = [
        "course_title",
        "course_organization",
        "course_Certificate_type",
        "course_difficulty",
    ]

    for column in text_columns:
        df[column] = (
            df[column]
            .astype(str)
            .str.strip()
            .str.lower()
        )

    # Save cleaned dataset
    PROCESSED_DATA.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DATA, index=False)

    print(f"Cleaned Shape : {df.shape}")
    print(f"Saved to : {PROCESSED_DATA}")


if __name__ == "__main__":
    clean_dataset()