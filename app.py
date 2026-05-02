from flask import Flask, render_template, request, redirect, flash
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "secret123"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE_DIR, "movies.csv")

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store"
    return response

# -------------------------------
# LOAD + PREPROCESS DATA
# -------------------------------
def load_data():
    df = pd.read_csv(FILE, engine='python')

    # Remove null
    df.dropna(inplace=True)

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Uppercase movie names
    df["Movie"] = df["Movie"].str.upper()

    # Reset index for proper serial number
    df.reset_index(drop=True, inplace=True)

    # Add ID (serial number)
    df["ID"] = df.index + 1

    return df

@app.route("/delete/<int:id>")
def delete(id):
    df = pd.read_csv(FILE)

    df.drop(index=id-1, inplace=True)
    df.to_csv(FILE, index=False)

    flash("Movie Deleted Successfully!")
    return redirect("/")


# -------------------------------
# HOME
# -------------------------------
@app.route("/")
def home():
    df = load_data()

    search = request.args.get("search")

    if search:
        df = df[df["Movie"].str.contains(search.upper())]

    data = df.to_dict(orient="records")

    # Aggregate functions
    avg_rating = round(df["Rating"].mean(), 2)
    total_movies = len(df)
    max_rating = df["Rating"].max()
    min_rating = df["Rating"].min()

    top_movie = df.loc[df["Rating"].idxmax()]

    # Quantile (Top 10%)
    top_10 = df.sort_values(by="Rating", ascending=False).head(5)
    top10_movies = top_10.to_dict(orient="records")

    # Recommendation (conditioning)
    recommended = df[df["Rating"] > 8]
    recommended_movies = recommended.to_dict(orient="records")

    # Chart data
    genre_counts = df["Genre"].value_counts().to_dict()

    # Stats
    stats = df.describe().to_string()

    return render_template("index.html",
                           movies=data,
                           avg=avg_rating,
                           top=top_movie,
                           total=total_movies,
                           max=max_rating,
                           min=min_rating,
                           recommended=recommended_movies,
                           top10=top10_movies,
                           stats=stats,
                           genre_counts=genre_counts)


# -------------------------------
# ADD MOVIE
# -------------------------------
@app.route("/add", methods=["POST"])
def add():
    movie = request.form["movie"].upper()
    genre = request.form["genre"]
    rating = float(request.form["rating"])

    # Constraint
    if rating < 0 or rating > 10:
        return "Invalid Rating"

    # Read raw CSV
    df = pd.read_csv(FILE, engine='python')

    # Add new row
    new_row = pd.DataFrame([[movie, genre, rating]],
                           columns=["Movie", "Genre", "Rating"])

    df = pd.concat([df, new_row], ignore_index=True)

    # Save
    df.to_csv(FILE, index=False)

    flash("Movie Added Successfully!")

    return redirect("/?updated=1", code=303)
    


# -------------------------------
# RUN
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
    