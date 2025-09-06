class Movie {
  constructor(id, title, genre, releaseYear) {
    this.id = id;                 // identificador único de la película
    this.title = title;           // título de la película
    this.genre = genre;           // género (acción, drama, comedia...)
    this.releaseYear = releaseYear; // año de estreno
  }

  updateDetails({ title, genre, releaseYear }) {
    if (title) this.title = title;
    if (genre) this.genre = genre;
    if (releaseYear) this.releaseYear = releaseYear;

    return this;
  }
}

module.exports = Movie;
