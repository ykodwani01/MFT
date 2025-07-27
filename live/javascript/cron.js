const cron = require('node-cron');
const fs = require('fs');
const { exec } = require('child_process');

const POSITIONS_FILE = '../../positions.json';

// This is a mock function to place a sell order.
// TODO: Replace this with the actual Motilal Oswal API integration.
function placeSellOrder(position) {
  console.log(`Placing sell order for ${position.symbol} at ${position.target_price}`);
}

function checkOrderFulfillment() {
  exec('python ../main.py', (error, stdout, stderr) => {
    if (error) {
      console.error(`exec error: ${error}`);
      return;
    }
    console.log(`stdout: ${stdout}`);
    console.error(`stderr: ${stderr}`);
  });
}

// Schedule a cron job to run every day at 5:00 PM
cron.schedule('0 17 * * *', () => {
  console.log('Running cron job to check order fulfillment and place new sell orders');

  checkOrderFulfillment();

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
