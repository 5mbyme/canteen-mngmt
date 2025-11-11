import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { AuthProvider, useAuth } from '../AuthContext';
import * as firebaseAuth from 'firebase/auth';

// Mock Firebase auth module
jest.mock('firebase/auth');

describe('AuthContext', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('AuthProvider renders children', () => {
    firebaseAuth.onAuthStateChanged.mockImplementation((auth, callback) => {
      callback(null);
      return jest.fn();
    });

    render(
      <AuthProvider>
        <div>Test Child</div>
      </AuthProvider>
    );

    expect(screen.getByText('Test Child')).toBeInTheDocument();
  });

  test('useAuth hook returns context value', async () => {
    const TestComponent = () => {
      const { currentUser } = useAuth();
      return <div>{currentUser ? 'Logged In' : 'Not Logged In'}</div>;
    };

    firebaseAuth.onAuthStateChanged.mockImplementation((auth, callback) => {
      callback(null);
      return jest.fn();
    });

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('Not Logged In')).toBeInTheDocument();
    });
  });

  test('useAuth throws error when used outside AuthProvider', () => {
    const TestComponent = () => {
      useAuth();
      return <div>Test</div>;
    };

    // Suppress console error for this test
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

    expect(() => {
      render(<TestComponent />);
    }).toThrow('useAuth must be used within AuthProvider');

    consoleSpy.mockRestore();
  });
});
