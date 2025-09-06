package com.peliculiando.app.Controller;

import com.peliculiando.app.DTO.UserDTO;
import com.peliculiando.app.Entity.User;
import com.peliculiando.app.Mapper.UserMapper;
import com.peliculiando.app.Service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;
    private final UserMapper userMapper;

    @PostMapping
    public ResponseEntity<UserDTO> createUser(@RequestBody UserDTO userDTO) {
        User user = userMapper.toEntity(userDTO);
        User created = userService.createUser(user);
        return ResponseEntity.ok(userMapper.toDTO(created));
    }

    @GetMapping("/{id}")
    public ResponseEntity<UserDTO> getUserById(@PathVariable Long id) {
        return ResponseEntity.ok(userMapper.toDTO(userService.getUserById(id)));
    }

    @GetMapping
    public ResponseEntity<List<UserDTO>> getAllUsers() {
        return ResponseEntity.ok(
                userService.getAllUsers().stream().map(userMapper::toDTO).toList()
        );
    }
}
