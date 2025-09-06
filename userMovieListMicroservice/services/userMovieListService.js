const userMovieListRepository = require('../repositories/userMovieListRepository');

function getUserMovies(userId) {
  return userMovieListRepository.findByUserId(userId);
}

function addUserMovie(data) {
  return userMovieListRepository.add(data);
}

function deleteUserMovie(userId, movieId) {
  return userMovieListRepository.remove(userId, movieId);
}

function updateUserMovie(userId, movieId, status) {
  return userMovieListRepository.update(userId, movieId, status);
}

module.exports = {
  getUserMovies,
  addUserMovie,
  deleteUserMovie,
  updateUserMovie,
};
