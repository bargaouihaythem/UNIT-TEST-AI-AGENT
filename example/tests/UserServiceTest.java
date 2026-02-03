package com.example.service;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import com.example.service.UserService.User;
import java.util.List;
import java.util.Optional;
import static org.junit.jupiter.api.Assertions.*;

class UserServiceTest {
    
    private UserService userService;

    @BeforeEach
    void setUp() {
        userService = new UserService();
    }

    // Tests for createUser()
    @Test
    void testCreateUserWithValidData() {
        User user = userService.createUser("John Doe", "john@example.com", "user");
        assertNotNull(user);
        assertEquals("John Doe", user.getName());
        assertEquals("john@example.com", user.getEmail());
    }

    @Test
    void testCreateUserWithInvalidEmailThrowsException() {
        assertThrows(IllegalArgumentException.class, 
            () -> userService.createUser("John", "invalid-email", "user"));
    }

    // Tests for getAllUsers()
    @Test
    void testGetAllUsersReturnsEmptyListInitially() {
        List<User> users = userService.getAllUsers();
        assertTrue(users.isEmpty());
    }

    @Test
    void testGetAllUsersReturnsAllCreatedUsers() {
        userService.createUser("John", "john@example.com", "user");
        userService.createUser("Jane", "jane@example.com", "admin");
        
        List<User> users = userService.getAllUsers();
        assertEquals(2, users.size());
    }

    // Tests for findUserById()
    @Test
    void testFindUserByIdReturnsUser() {
        User created = userService.createUser("John", "john@example.com", "user");
        Optional<User> found = userService.findUserById(created.getId());
        
        assertTrue(found.isPresent());
        assertEquals("John", found.get().getName());
    }

    @Test
    void testFindUserByIdReturnsEmptyForNonExistent() {
        Optional<User> found = userService.findUserById(999L);
        assertFalse(found.isPresent());
    }

    // Tests for deleteUser()
    @Test
    void testDeleteUserRemovesUser() {
        User user = userService.createUser("John", "john@example.com", "user");
        boolean deleted = userService.deleteUser(user.getId());
        
        assertTrue(deleted);
        assertEquals(0, userService.getAllUsers().size());
    }

    @Test
    void testDeleteNonExistentUserReturnsFalse() {
        boolean deleted = userService.deleteUser(999L);
        assertFalse(deleted);
    }

    // Tests for isAdmin()
    @Test
    void testIsAdminReturnsTrueForAdminRole() {
        User admin = userService.createUser("Admin", "admin@example.com", "admin");
        assertTrue(userService.isAdmin(admin));
    }

    @Test
    void testIsAdminReturnsFalseForUserRole() {
        User user = userService.createUser("User", "user@example.com", "user");
        assertFalse(userService.isAdmin(user));
    }

    // Tests for isValidEmail()
    @Test
    void testIsValidEmailWithCorrectFormat() {
        assertTrue(userService.isValidEmail("test@example.com"));
    }

    @Test
    void testIsValidEmailRejectsInvalidFormat() {
        assertFalse(userService.isValidEmail("invalid-email"));
    }

    @Test
    void testIsValidEmailRejectsEmptyString() {
        assertFalse(userService.isValidEmail(""));
    }

    @Test
    void testIsValidEmailRejectsNull() {
        assertFalse(userService.isValidEmail(null));
    }

    @Test
    void testIsValidEmailWithSubdomain() {
        assertTrue(userService.isValidEmail("user@mail.example.com"));
    }
}
