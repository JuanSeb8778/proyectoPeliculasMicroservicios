package com.peliculiando.reviewsMicroservice.Service;

import com.peliculiando.reviewsMicroservice.Entity.Review;
import com.peliculiando.reviewsMicroservice.Repository.ReviewRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class ReviewService {

    private final ReviewRepository reviewRepository;

    public Review createReview(Review review) {
        return reviewRepository.save(review);
    }

    public Review getReviewById(Long id) {
        return reviewRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Review not found"));
    }

    public List<Review> getAllReviews() {
        return reviewRepository.findAll();
    }

    public List<Review> getReviewsByMovie(Long movieId) {
        return reviewRepository.findByMovieId(movieId);
    }

    public List<Review> getReviewsByUser(Long userId) {
        return reviewRepository.findByUserId(userId);
    }

    public Review updateReview(Long id, Review updatedReview) {
        Review existing = getReviewById(id);
        existing.setRating(updatedReview.getRating());
        existing.setComment(updatedReview.getComment());
        return reviewRepository.save(existing);
    }

    public void deleteReview(Long id) {
        reviewRepository.deleteById(id);
    }
}

