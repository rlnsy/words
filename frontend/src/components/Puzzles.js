import React from 'react'

class Puzzles extends React.Component {
	
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      items: []
    };
  }

  componentDidMount() {
    fetch("http://127.0.0.1:8000/api/puzzles")
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            items: result.results
          });
        },
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )
  }

  render() {
    const { error, isLoaded, items } = this.state;
    if (error) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <div>Loading...</div>;
    } else {
      return (
				<div>
					<h1> Puzzles: </h1>
					<ul>
						{items.map(item => (
							<li key={item.title}>
								{item.name} {item.title}
							</li>
						))}
					</ul>
				</div>
      );
    }
  }
}

export default Puzzles