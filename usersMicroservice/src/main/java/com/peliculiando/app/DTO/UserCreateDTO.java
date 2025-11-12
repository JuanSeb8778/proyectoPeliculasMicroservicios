package com.peliculiando.app.DTO;

import lombok.Data;

@Data
public class UserCreateDTO {
    private String firstName;
    private String lastName;
    private String email;
    private String password;
    private String username;
    private Long phoneNumber;
}
