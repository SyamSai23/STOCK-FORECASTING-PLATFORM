const abbreviateNumber = (num, fixed) => {
  if (!num) {
    return '-';
  }
  if (num === 0) {
    return '$ 0';
  }
  fixed = !fixed || fixed < 0 ? 0 : fixed;
  var b = num.toPrecision(2).split('e'),
    k = b.length === 1 ? 0 : Math.floor(Math.min(b[1].slice(1), 14) / 3),
    c = k < 1 ? num.toFixed(0 + fixed) : (num / Math.pow(10, k * 3)).toFixed(1 + fixed),
    d = c < 0 ? c : Math.abs(c),
    e = d + ['', ' K', ' M', ' B', ' T'][k];
  if (k === 0) {
    e = `$ ${e}`;
  }
  return e;
};

export default abbreviateNumber;
