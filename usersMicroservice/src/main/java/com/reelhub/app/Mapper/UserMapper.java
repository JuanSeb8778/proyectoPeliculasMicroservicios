package com.reelhub.app.Mapper;

import com.reelhub.app.DTO.UserCreateDTO;
import com.reelhub.app.DTO.UserDTO;
import com.reelhub.app.Entity.User;
import org.mapstruct.Mapper;


@Mapper(componentModel = "spring")
public interface UserMapper {
    UserDTO toDTO(User user);
    User toEntity(UserCreateDTO dto);
}
