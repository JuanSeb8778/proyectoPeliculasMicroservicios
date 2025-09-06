class UserMovieList {
  constructor(userId) {
    this.userId = userId;
    this.movies = []; // [{ movieId, status }]
  }

  addMovie(movieId, status = 'pending') {
    const movie = { movieId, status };
    this.movies.push(movie);
    return movie;
  }

  removeMovie(movieId) {
    this.movies = this.movies.filter(m => m.movieId !== movieId);
    return { message: `Película ${movieId} eliminada` };
  }

  updateMovie(movieId, status) {
    const movie = this.movies.find(m => m.movieId === movieId);
    if (movie) {
      movie.status = status;
      return movie;
    }
    return { message: `Película ${movieId} no encontrada` };
  }

  getMovies() {
    return {
      userId: this.userId,
      movies: this.movies
    };
  }
}

module.exports = UserMovieList;
