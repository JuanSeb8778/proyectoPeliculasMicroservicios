package com.peliculiando.reviewsMicroservice.Controlller;

import com.peliculiando.reviewsMicroservice.DTO.CreateReviewRequest;
import com.peliculiando.reviewsMicroservice.DTO.ReviewDTO;
import com.peliculiando.reviewsMicroservice.Entity.Review;
import com.peliculiando.reviewsMicroservice.Mapper.ReviewMapper;
import com.peliculiando.reviewsMicroservice.Service.ReviewService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/reviews")
@RequiredArgsConstructor
public class ReviewController {

    private final ReviewService reviewService;
    private final ReviewMapper reviewMapper;

    @PostMapping
    @Operation(summary = "Crear una nueva reseña")
    @ApiResponse(responseCode = "201", description = "Reseña creada exitosamente")
    @ApiResponse(responseCode = "400", description = "Datos de reseña inválidos")
    public ResponseEntity<ReviewDTO> createReview(@RequestBody CreateReviewRequest request) {
        Review review = reviewMapper.toEntity(request);
        Review created = reviewService.createReview(review);
        return ResponseEntity.ok(reviewMapper.toDTO(created));
    }

    @GetMapping("/{id}")
    @Operation(summary = "Obtener reseña por ID")
    @ApiResponse(responseCode = "200", description = "Reseña encontrada")
    @ApiResponse(responseCode = "404", description = "Reseña no encontrada")
    public ResponseEntity<ReviewDTO> getReviewById(@PathVariable Long id) {
        return ResponseEntity.ok(reviewMapper.toDTO(reviewService.getReviewById(id)));
    }

    @GetMapping
    @Operation(summary = "Obtener todas las reseñas")
    @ApiResponse(responseCode = "200", description = "Lista de reseñas encontrada")
    public ResponseEntity<List<ReviewDTO>> getAllReviews() {
        return ResponseEntity.ok(
                reviewService.getAllReviews().stream().map(reviewMapper::toDTO).toList()
        );
    }

    @GetMapping("/movie/{movieId}")
    @Operation(summary = "Obtener reseña por ID de pelicula")
    @ApiResponse(responseCode = "200", description = "Reseña encontrada")
    @ApiResponse(responseCode = "404", description = "Reseña no encontrada")
    public ResponseEntity<List<ReviewDTO>> getReviewsByMovie(@PathVariable Long movieId) {
        return ResponseEntity.ok(
                reviewService.getReviewsByMovie(movieId).stream().map(reviewMapper::toDTO).toList()
        );
    }

    @GetMapping("/user/{userId}")
    @Operation(summary = "Obtener reseña por ID de usuario")
    @ApiResponse(responseCode = "200", description = "Reseña encontrada")
    @ApiResponse(responseCode = "404", description = "Reseña no encontrada")
    public ResponseEntity<List<ReviewDTO>> getReviewsByUser(@PathVariable Long userId) {
        return ResponseEntity.ok(
                reviewService.getReviewsByUser(userId).stream().map(reviewMapper::toDTO).toList()
        );
    }

    @PutMapping("/{id}")
    @Operation(summary = "Actualizar una reseña existente")
    @ApiResponse(responseCode = "200", description = "Reseña actualizada")
    @ApiResponse(responseCode = "404", description = "Reseña no encontrada")
    public ResponseEntity<ReviewDTO> updateReview(@PathVariable Long id, @RequestBody ReviewDTO reviewDTO) {
        Review review = reviewMapper.toEntity(reviewDTO);
        Review updated = reviewService.updateReview(id, review);
        return ResponseEntity.ok(reviewMapper.toDTO(updated));
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Eliminar una reseña")
    @ApiResponse(responseCode = "204", description = "Reseña eliminada")
    @ApiResponse(responseCode = "404", description = "Reseña no encontrada")
    public ResponseEntity<Void> deleteReview(@PathVariable Long id) {
        reviewService.deleteReview(id);
        return ResponseEntity.noContent().build();
    }
}

