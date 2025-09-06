package com.peliculiando.reviewsMicroservice.Mapper;

import com.peliculiando.reviewsMicroservice.DTO.CreateReviewRequest;
import com.peliculiando.reviewsMicroservice.DTO.ReviewDTO;
import com.peliculiando.reviewsMicroservice.Entity.Review;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring")
public interface ReviewMapper {
    ReviewDTO toDTO(Review review);

    @Mapping(target = "id", ignore = true)
    Review toEntity(CreateReviewRequest request);

    Review toEntity(ReviewDTO dto);
}

