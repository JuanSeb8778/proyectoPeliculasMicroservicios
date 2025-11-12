const movieRepository = require('../repositories/movieRepository');

async function getAllMovies() {
  return await movieRepository.findAll();
}

async function getMovieById(id) {
  return await movieRepository.findById(id);
}

async function addMovie(data) {
  return await movieRepository.add(data);
}

async function updateMovie(id, data) {
  return await movieRepository.update(id, data);
}

async function deleteMovie(id) {
  return await movieRepository.remove(id);
}

module.exports = {
  getAllMovies,
  getMovieById,
  addMovie,
  updateMovie,
  deleteMovie,
};
