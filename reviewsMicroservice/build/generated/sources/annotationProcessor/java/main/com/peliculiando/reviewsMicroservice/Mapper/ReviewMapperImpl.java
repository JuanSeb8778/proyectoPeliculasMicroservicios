package com.peliculiando.reviewsMicroservice.Mapper;

import com.peliculiando.reviewsMicroservice.DTO.CreateReviewRequest;
import com.peliculiando.reviewsMicroservice.DTO.ReviewDTO;
import com.peliculiando.reviewsMicroservice.Entity.Review;
import javax.annotation.processing.Generated;
import org.springframework.stereotype.Component;

@Generated(
    value = "org.mapstruct.ap.MappingProcessor",
    date = "2025-09-06T02:42:12-0500",
    comments = "version: 1.5.5.Final, compiler: IncrementalProcessingEnvironment from gradle-language-java-8.14.3.jar, environment: Java 21.0.7 (Microsoft)"
)
@Component
public class ReviewMapperImpl implements ReviewMapper {

    @Override
    public ReviewDTO toDTO(Review review) {
        if ( review == null ) {
            return null;
        }

        ReviewDTO reviewDTO = new ReviewDTO();

        reviewDTO.setId( review.getId() );
        reviewDTO.setUserId( review.getUserId() );
        reviewDTO.setMovieId( review.getMovieId() );
        reviewDTO.setRating( review.getRating() );
        reviewDTO.setComment( review.getComment() );
        reviewDTO.setCreatedAt( review.getCreatedAt() );
        reviewDTO.setUpdatedAt( review.getUpdatedAt() );

        return reviewDTO;
    }

    @Override
    public Review toEntity(CreateReviewRequest request) {
        if ( request == null ) {
            return null;
        }

        Review review = new Review();

        review.setUserId( request.getUserId() );
        review.setMovieId( request.getMovieId() );
        review.setRating( request.getRating() );
        review.setComment( request.getComment() );

        return review;
    }

    @Override
    public Review toEntity(ReviewDTO dto) {
        if ( dto == null ) {
            return null;
        }

        Review review = new Review();

        review.setId( dto.getId() );
        review.setUserId( dto.getUserId() );
        review.setMovieId( dto.getMovieId() );
        review.setRating( dto.getRating() );
        review.setComment( dto.getComment() );
        review.setCreatedAt( dto.getCreatedAt() );
        review.setUpdatedAt( dto.getUpdatedAt() );

        return review;
    }
}
