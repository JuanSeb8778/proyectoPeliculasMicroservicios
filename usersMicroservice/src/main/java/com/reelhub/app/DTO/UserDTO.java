package com.reelhub.app.DTO;

import lombok.Data;

import java.time.LocalDate;

@Data
public class UserDTO {

    private String id;
    private String firstName;
    private String lastName;
    private String email;
    private String username;
    private Long phoneNumber;

}
