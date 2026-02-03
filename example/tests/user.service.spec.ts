import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { UserService, User } from './user.service';

describe('UserService', () => {
  let service: UserService;
  let httpMock: HttpTestingController;
  const apiUrl = 'https://api.example.com/users';

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [UserService]
    });
    service = TestBed.inject(UserService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  // Tests for getUsers()
  it('should retrieve all users from API', () => {
    const mockUsers: User[] = [
      { id: 1, name: 'John', email: 'john@example.com', role: 'user' },
      { id: 2, name: 'Jane', email: 'jane@example.com', role: 'admin' }
    ];

    service.getUsers().subscribe(users => {
      expect(users.length).toBe(2);
      expect(users).toEqual(mockUsers);
    });

    const req = httpMock.expectOne(apiUrl);
    expect(req.request.method).toBe('GET');
    req.flush(mockUsers);
  });

  // Tests for getUserById()
  it('should retrieve user by id', () => {
    const mockUser: User = { id: 1, name: 'John', email: 'john@example.com', role: 'user' };

    service.getUserById(1).subscribe(user => {
      expect(user).toEqual(mockUser);
    });

    const req = httpMock.expectOne(`${apiUrl}/1`);
    expect(req.request.method).toBe('GET');
    req.flush(mockUser);
  });

  // Tests for createUser()
  it('should create a new user', () => {
    const newUser: User = { id: 0, name: 'Bob', email: 'bob@example.com', role: 'user' };
    const createdUser: User = { ...newUser, id: 3 };

    service.createUser(newUser).subscribe(user => {
      expect(user.id).toBe(3);
      expect(user.name).toBe('Bob');
    });

    const req = httpMock.expectOne(apiUrl);
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual(newUser);
    req.flush(createdUser);
  });

  // Tests for updateUser()
  it('should update existing user', () => {
    const updatedUser: User = { id: 1, name: 'John Updated', email: 'john.new@example.com', role: 'admin' };

    service.updateUser(1, updatedUser).subscribe(user => {
      expect(user.name).toBe('John Updated');
      expect(user.role).toBe('admin');
    });

    const req = httpMock.expectOne(`${apiUrl}/1`);
    expect(req.request.method).toBe('PUT');
    req.flush(updatedUser);
  });

  // Tests for deleteUser()
  it('should delete user', () => {
    service.deleteUser(1).subscribe();

    const req = httpMock.expectOne(`${apiUrl}/1`);
    expect(req.request.method).toBe('DELETE');
    req.flush(null);
  });

  // Tests for isAdmin()
  it('should return true for admin user', () => {
    const adminUser: User = { id: 1, name: 'Admin', email: 'admin@example.com', role: 'admin' };
    expect(service.isAdmin(adminUser)).toBe(true);
  });

  it('should return false for non-admin user', () => {
    const regularUser: User = { id: 2, name: 'User', email: 'user@example.com', role: 'user' };
    expect(service.isAdmin(regularUser)).toBe(false);
  });

  // Tests for validateEmail()
  it('should validate correct email', () => {
    expect(service.validateEmail('test@example.com')).toBe(true);
  });

  it('should reject email without @', () => {
    expect(service.validateEmail('testexample.com')).toBe(false);
  });

  it('should reject email without domain', () => {
    expect(service.validateEmail('test@')).toBe(false);
  });

  it('should reject empty email', () => {
    expect(service.validateEmail('')).toBe(false);
  });

  it('should reject email with spaces', () => {
    expect(service.validateEmail('test @example.com')).toBe(false);
  });
});
