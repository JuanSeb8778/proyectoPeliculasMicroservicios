package com.reelhub.reviewsMicroservice.Mapper;

import com.reelhub.reviewsMicroservice.DTO.CreateReviewRequest;
import com.reelhub.reviewsMicroservice.DTO.ReviewDTO;
import com.reelhub.reviewsMicroservice.Entity.Review;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring")
public interface ReviewMapper {
    ReviewDTO toDTO(Review review);

    @Mapping(target = "id", ignore = true)
    Review toEntity(CreateReviewRequest request);

    Review toEntity(ReviewDTO dto);
}

