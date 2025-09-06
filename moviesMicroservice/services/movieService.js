// services/movieService.js
const movieRepository = require('../repositories/movieRepository');

function getAllMovies() {
  return movieRepository.findAll();
}

function getMovieById(id) {
  return movieRepository.findById(id);
}

function addMovie(data) {
  return movieRepository.add(data);
}

function updateMovie(id, data) {
  return movieRepository.update(id, data);
}

function deleteMovie(id) {
  return movieRepository.remove(id);
}

module.exports = {
  getAllMovies,
  getMovieById,
  addMovie,
  updateMovie,
  deleteMovie,
};
