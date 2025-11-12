// repositories/movieRepository.js
const pool = require('../db');
const Movie = require('../entities/movie');

async function findAll() {
  const conn = await pool.getConnection();
  const rows = await conn.query('SELECT * FROM movies');
  conn.release();
  return rows.map(r => new Movie(r.id, r.title, r.genre, r.release_year));
}

async function findById(id) {
  const conn = await pool.getConnection();
  const rows = await conn.query('SELECT * FROM movies WHERE id = ?', [id]);
  conn.release();
  if (rows.length === 0) return null;
  const r = rows[0];
  return new Movie(r.id, r.title, r.genre, r.release_year);
}

async function add({ title, genre, releaseYear }) {
  const conn = await pool.getConnection();
  const result = await conn.query(
    'INSERT INTO movies (title, genre, release_year) VALUES (?, ?, ?)',
    [title, genre, releaseYear]
  );
  conn.release();
  return new Movie(result.insertId, title, genre, releaseYear);
}

async function update(id, { title, genre, releaseYear }) {
  const conn = await pool.getConnection();
  const result = await conn.query(
    'UPDATE movies SET title = ?, genre = ?, release_year = ? WHERE id = ?',
    [title, genre, releaseYear, id]
  );
  conn.release();
  if (result.affectedRows === 0) return null;
  return findById(id);
}

async function remove(id) {
  const conn = await pool.getConnection();
  const result = await conn.query('DELETE FROM movies WHERE id = ?', [id]);
  conn.release();
  if (result.affectedRows === 0) return { message: 'Película no encontrada' };
  return { message: `Película ${id} eliminada` };
}

module.exports = {
  findAll,
  findById,
  add,
  update,
  remove,
};
