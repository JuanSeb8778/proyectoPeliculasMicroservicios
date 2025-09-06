// routes/movieRouter.js
const express = require('express');
const router = express.Router();
const movieService = require('../services/movieService');

/**
 * @swagger
 * tags:
 *   name: Movies
 *   description: Gestión de películas
 */

/**
 * @swagger
 * /movies:
 *   get:
 *     summary: Obtener todas las películas
 *     tags: [Movies]
 *     responses:
 *       200:
 *         description: Lista de películas
 */
router.get('/', (req, res) => {
  res.json(movieService.getAllMovies());
});

/**
 * @swagger
 * /movies/{id}:
 *   get:
 *     summary: Obtener una película por ID
 *     tags: [Movies]
 *     parameters:
 *       - in: path
 *         name: id
 *         schema:
 *           type: string
 *         required: true
 *     responses:
 *       200:
 *         description: Película encontrada
 */
router.get('/:id', (req, res) => {
  const movie = movieService.getMovieById(req.params.id);
  if (movie) res.json(movie);
  else res.status(404).json({ message: 'Movie not found' });
});

/**
 * @swagger
 * /movies:
 *   post:
 *     summary: Agregar nueva película
 *     tags: [Movies]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               title:
 *                 type: string
 *               genre:
 *                 type: string
 *               year:
 *                 type: number
 *     responses:
 *       201:
 *         description: Película agregada
 */
router.post('/', (req, res) => {
  const movie = movieService.addMovie(req.body);
  res.status(201).json(movie);
});

/**
 * @swagger
 * /movies/{id}:
 *   put:
 *     summary: Actualizar película por ID
 *     tags: [Movies]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               title:
 *                 type: string
 *               genre:
 *                 type: string
 *               year:
 *                 type: number
 *     responses:
 *       200:
 *         description: Película actualizada
 */
router.put('/:id', (req, res) => {
  const updated = movieService.updateMovie(req.params.id, req.body);
  if (updated) res.json(updated);
  else res.status(404).json({ message: 'Movie not found' });
});

/**
 * @swagger
 * /movies/{id}:
 *   delete:
 *     summary: Eliminar película por ID
 *     tags: [Movies]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *     responses:
 *       200:
 *         description: Película eliminada
 */
router.delete('/:id', (req, res) => {
  const deleted = movieService.deleteMovie(req.params.id);
  if (deleted) res.json(deleted);
  else res.status(404).json({ message: 'Movie not found' });
});

module.exports = router;
