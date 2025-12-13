import { Component } from 'react';
import ErrorImg from './../../assets/error.jpg';

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return <img style={{ width: '100vw', height: '100vh', objectFit: 'contain' }} src={ErrorImg} alt='error' />;
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
