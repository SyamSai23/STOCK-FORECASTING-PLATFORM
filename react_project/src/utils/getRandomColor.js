const getRandomColor = () => {
  const colors = [
    '#1f77b4', '#2ca02c', '#9467bd', '#8c564b', '#e377c2',
    '#7f7f7f', '#bcbd22', '#17becf', '#aec7e8', '#ffbb78', '#98df8a',
    '#c5b0d5', '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5'
  ];

  return colors[Math.floor(Math.random() * colors.length)];
};

export default getRandomColor;
