const Movie = require('../entities/movie');

let movies = [];

function findAll() {
  return movies;
}

function findById(id) {
  return movies.find(m => m.id === id);
}

function add({ id, title, genre, releaseYear }) {
  const movie = new Movie(id, title, genre, releaseYear);
  movies.push(movie);
  return movie;
}

function update(id, data) {
  const movie = movies.find(m => m.id === id);
  if (movie) {
    return movie.updateDetails(data);
  }
  return { message: 'Película no encontrada' };
}

function remove(id) {
  movies = movies.filter(m => m.id !== id);
  return { message: `Película ${id} eliminada` };
}

module.exports = {
  findAll,
  findById,
  add,
  update,
  remove,
};
