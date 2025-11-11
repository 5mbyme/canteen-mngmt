import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../App';
import * as firebaseAuth from 'firebase/auth';

jest.mock('firebase/auth');

describe('App Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    firebaseAuth.onAuthStateChanged.mockImplementation((auth, callback) => {
      callback(null);
      return jest.fn();
    });
  });

  test('renders without crashing', () => {
    render(<App />);
    expect(screen.getByRole('main') || screen.getByText(/canteen/i)).toBeInTheDocument();
  });
});
