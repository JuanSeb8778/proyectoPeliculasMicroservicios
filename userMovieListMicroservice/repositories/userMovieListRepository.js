const UserMovieList = require('../entities/userMovieList');

let userMovieLists = [];

function findByUserId(userId) {
  let userList = userMovieLists.find(list => list.userId === userId);
  if (!userList) {
    userList = new UserMovieList(userId);
    userMovieLists.push(userList);
  }
  return userList.getMovies();
}

function add({ userId, movieId, status }) {
  let userList = userMovieLists.find(list => list.userId === userId);
  if (!userList) {
    userList = new UserMovieList(userId);
    userMovieLists.push(userList);
  }
  userList.addMovie(movieId, status);
  return userList.getMovies();
}

function remove(userId, movieId) {
  const userList = userMovieLists.find(list => list.userId === userId);
  if (userList) {
    userList.removeMovie(movieId);
    return userList.getMovies();
  }
  return { message: 'Usuario no encontrado' };
}

function update(userId, movieId, status) {
  const userList = userMovieLists.find(list => list.userId === userId);
  if (userList) {
    userList.updateMovie(movieId, status);
    return userList.getMovies();
  }
  return { message: 'Usuario no encontrado' };
}

module.exports = {
  findByUserId,
  add,
  remove,
  update,
};
