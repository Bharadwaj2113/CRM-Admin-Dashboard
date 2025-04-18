import { render, screen } from '@testing-library/react';
import App from './App';
import '@testing-library/jest-dom';

test('renders the app component', () => {
  render(<App />);
  const appElement = screen.getByText(/crm/i);
  expect(appElement).toBeInTheDocument();
});