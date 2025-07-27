const cron = require('node-cron');
const fs = require('fs');

const POSITIONS_FILE = '../../positions.json';

// This is a mock function to place a sell order.
// TODO: Replace this with the actual Motilal Oswal API integration.
function placeSellOrder(position) {
  console.log(`Placing sell order for ${position.symbol} at ${position.target_price}`);
}

// Schedule a cron job to run every day at 9:00 AM
cron.schedule('0 9 * * *', () => {
  console.log('Running cron job to place sell orders');

  fs.readFile(POSITIONS_FILE, 'utf8', (err, data) => {
    if (err) {
      console.error('Error reading positions file:', err);
      return;
    }

    const positions = JSON.parse(data);

    positions.forEach(position => {
      if (position.status === 'open') {
        placeSellOrder(position);
      }
    });
  });
});
