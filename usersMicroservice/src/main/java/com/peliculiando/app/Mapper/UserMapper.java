package com.peliculiando.app.Mapper;

import com.peliculiando.app.DTO.UserCreateDTO;
import com.peliculiando.app.DTO.UserDTO;
import com.peliculiando.app.Entity.User;
import org.mapstruct.Mapper;


@Mapper(componentModel = "spring")
public interface UserMapper {
    UserDTO toDTO(User user);
    User toEntity(UserCreateDTO dto);
}
