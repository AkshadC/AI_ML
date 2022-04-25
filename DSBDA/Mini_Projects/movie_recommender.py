import pandas as pd
import warnings
from tabulate import tabulate


class movie_recommender:

    def __init__(self, movies_df: pd.DataFrame, rating_df: pd.DataFrame):
        self.movies_df = movies_df
        self.rating_df = rating_df

    def preprocessing_data(self):
        self.movies_df['year'] = self.movies_df.title.str.extract('(\(\d\d\d\d\))', expand=False)
        self.movies_df['year'] = self.movies_df.year.str.extract('(\d\d\d\d)', expand=False)
        self.movies_df['title'] = self.movies_df.title.str.replace('(\(\d\d\d\d\))', '')
        self.movies_df['title'] = self.movies_df['title'].apply(lambda x: x.strip())
        self.movies_df['title'] = self.movies_df['title'].map(lambda x: x.lower() if isinstance(x, str) else x)

    def genre_processing(self):
        self.movies_df['genres'] = self.movies_df.genres.str.split('|')
        movies_with_genres = self.movies_df.copy()
        for index, row in self.movies_df.iterrows():
            for genre in row['genres']:
                movies_with_genres.at[index, genre] = 1
        movies_with_genres = movies_with_genres.fillna(0)
        self.rating_df = self.rating_df.drop(['timestamp'], axis=1)
        return movies_with_genres

    def user_movies(self):
        titles = self.movies_df['title'].to_numpy()
        print("ENTER MOVIE NAMES WITH RATINGS ")
        print("_" * 100)
        n = int(input("Enter the number of movies you want to rate : "))
        user_input = list()
        for i in range(n):
            movie = input("Enter the movie name: ")
            rating = 0.0
            movie = movie.lower()
            if movie in titles:
                rating = float(input("Enter the rating for the movie from 0 - 5: "))
                movie_name = {'title': movie, 'rating': rating}
                user_input.append(movie_name)
            elif len(self.movies_df.loc[self.movies_df['title'].str.contains(movie, case=False)]['title']) >= 1:
                movies_similar = self.movies_df.loc[self.movies_df['title'].str.contains(movie, case=False)][
                    ['movieId', 'title']]
                print(tabulate(movies_similar, headers='keys', tablefmt='psql'))
                movie_id = input("Choose movie id from these list of movies : else enter 0 : ")

                if movie == 0:
                    continue
                else:
                    query = "movieId ==" + movie_id
                    movie = (self.movies_df.query(query)['title']).to_numpy()[0]
                    print("Enter the rating for the movie from 0 - 5: ", end="")
                    rating = float(input())
                    movie_name = {'title': movie, 'rating': rating}
                    user_input.append(movie_name)
            else:
                print("We have not yet rated this movie please enter another movie please!!")
                n = n + 1
        return user_input

    def recommend_movies(self, user_input, movies_with_genres):
        input_movies = pd.DataFrame(user_input)
        input_id = self.movies_df[self.movies_df['title'].isin(input_movies['title'].tolist())]
        input_movies = pd.merge(input_id, input_movies)
        input_movies = input_movies.drop('genres', 1).drop('year', 1)

        user_movies = movies_with_genres[movies_with_genres['movieId'].isin(input_movies['movieId'].tolist())]
        userMovies = user_movies.reset_index(drop=True)
        user_genre_table = userMovies.drop('movieId', 1).drop('title', 1).drop('genres', 1).drop('year', 1)
        genre_table = movies_with_genres.set_index(movies_with_genres['movieId'])
        genre_table = genre_table.drop('movieId', 1).drop('title', 1).drop('genres', 1).drop('year', 1)
        user_profile = user_genre_table.transpose().dot(input_movies['rating'])
        recommendation_table = ((genre_table * user_profile).sum(axis=1)) / (user_profile.sum())
        recommendation_table = recommendation_table.sort_values(ascending=False)

        print("\nTHE MOVIES YOU RATED ARE : ")

        print(tabulate(userMovies.loc[:, (userMovies != 0.0).any(axis=0)], headers='keys', tablefmt='psql'))
        recommended_movies = self.movies_df.loc[self.movies_df['movieId'].isin(recommendation_table.head(5).keys())][
            ['title', 'genres']]
        return recommended_movies


def main():
    movies = pd.read_csv('Content_Based_Filtering_DataSets/movies.csv')
    ratings = pd.read_csv('Content_Based_Filtering_DataSets/ratings.csv')
    movie_object = movie_recommender(movies, ratings)
    movie_object.preprocessing_data()
    movies_with_genres = movie_object.genre_processing()
    user_input = movie_object.user_movies()
    recommended_movies = movie_object.recommend_movies(user_input, movies_with_genres)

    print("\nTHE MOVIES YOU MIGHT LIKE TO WATCH NEXT ARE : \n")
    print(tabulate(recommended_movies, headers='keys', tablefmt='psql'))


if __name__ == "__main__":
    main()
