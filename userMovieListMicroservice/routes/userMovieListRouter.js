const express = require('express');
const router = express.Router();
const userMovieListService = require('../services/userMovieListService');

/**
 * @swagger
 * /user-movie-list/{userId}:
 *   get:
 *     summary: Obtener lista de películas de un usuario
 *     tags: [UserMovieList]
 *     parameters:
 *       - in: path
 *         name: userId
 *         schema:
 *           type: string
 *         required: true
 *         description: ID del usuario
 *     responses:
 *       200:
 *         description: Devuelve userId y lista de películas
 */
router.get('/:userId', (req, res) => {
  const { userId } = req.params;
  const list = userMovieListService.getUserMovies(userId);
  res.json(list);
});

/**
 * @swagger
 * /user-movie-list:
 *   post:
 *     summary: Agregar película a la lista de un usuario
 *     tags: [UserMovieList]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               userId:
 *                 type: string
 *                 example: "123"
 *               movieId:
 *                 type: string
 *                 example: "456"
 *     responses:
 *       201:
 *         description: Película agregada
 */
router.post('/', (req, res) => {
  const entry = userMovieListService.addUserMovie(req.body);
  res.status(201).json(entry);
});

/**
 * @swagger
 * /user-movie-list/{userId}/{movieId}:
 *   delete:
 *     summary: Eliminar película de la lista de un usuario
 *     tags: [UserMovieList]
 *     parameters:
 *       - in: path
 *         name: userId
 *         schema:
 *           type: string
 *         required: true
 *         description: ID del usuario
 *       - in: path
 *         name: movieId
 *         schema:
 *           type: string
 *         required: true
 *         description: ID de la película
 *     responses:
 *       200:
 *         description: Película eliminada
 */
router.delete('/:userId/:movieId', (req, res) => {
  const { userId, movieId } = req.params;
  const result = userMovieListService.deleteUserMovie(userId, movieId);
  res.json(result);
});

/**
 * @swagger
 * /user-movie-list/{userId}/{movieId}:
 *   put:
 *     summary: Actualizar estado de película en la lista
 *     tags: [UserMovieList]
 *     parameters:
 *       - in: path
 *         name: userId
 *         schema:
 *           type: string
 *         required: true
 *         description: ID del usuario
 *       - in: path
 *         name: movieId
 *         schema:
 *           type: string
 *         required: true
 *         description: ID de la película
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               status:
 *                 type: string
 *                 example: "watched"
 *     responses:
 *       200:
 *         description: Estado actualizado
 */
router.put('/:userId/:movieId', (req, res) => {
  const { userId, movieId } = req.params;
  const { status } = req.body;
  const result = userMovieListService.updateUserMovie(userId, movieId, status);
  res.json(result);
});

module.exports = router;
