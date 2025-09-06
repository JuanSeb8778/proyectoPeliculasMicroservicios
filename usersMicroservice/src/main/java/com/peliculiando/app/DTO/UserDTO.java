package com.peliculiando.app.DTO;

import lombok.Data;

import java.time.LocalDate;

@Data
public class UserDTO {

    private Long id;
    private String firstName;
    private String lastName;
    private String email;
    private String username;
    private String phoneNumber;
    private String bio;
    private String profilePictureUrl;
    private String address;
    private LocalDate birthdate;


}
