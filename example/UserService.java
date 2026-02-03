package com.example.service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.regex.Pattern;

/**
 * Service for managing users.
 */
public class UserService {
    
    private List<User> users = new ArrayList<>();
    private static final Pattern EMAIL_PATTERN = Pattern.compile("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+$");

    public static class User {
        private Long id;
        private String name;
        private String email;
        private String role;

        public User(Long id, String name, String email, String role) {
            this.id = id;
            this.name = name;
            this.email = email;
            this.role = role;
        }

        public Long getId() { return id; }
        public String getName() { return name; }
        public String getEmail() { return email; }
        public String getRole() { return role; }
    }

    /**
     * Get all users.
     */
    public List<User> getAllUsers() {
        return new ArrayList<>(users);
    }

    /**
     * Find user by ID.
     */
    public Optional<User> findUserById(Long id) {
        return users.stream()
                .filter(u -> u.getId().equals(id))
                .findFirst();
    }

    /**
     * Create a new user.
     * @throws IllegalArgumentException if email is invalid
     */
    public User createUser(String name, String email, String role) {
        if (!isValidEmail(email)) {
            throw new IllegalArgumentException("Invalid email format");
        }
        Long newId = (long) (users.size() + 1);
        User user = new User(newId, name, email, role);
        users.add(user);
        return user;
    }

    /**
     * Delete user by ID.
     */
    public boolean deleteUser(Long id) {
        return users.removeIf(u -> u.getId().equals(id));
    }

    /**
     * Check if user is admin.
     */
    public boolean isAdmin(User user) {
        return "admin".equals(user.getRole());
    }

    /**
     * Validate email format.
     */
    public boolean isValidEmail(String email) {
        if (email == null || email.isEmpty()) {
            return false;
        }
        return EMAIL_PATTERN.matcher(email).matches();
    }
}
