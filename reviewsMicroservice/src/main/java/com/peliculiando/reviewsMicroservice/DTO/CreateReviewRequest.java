package com.peliculiando.reviewsMicroservice.DTO;

import lombok.Data;

@Data
public class CreateReviewRequest {
    private Long userId;
    private Long movieId;
    private Integer rating;
    private String comment;
}