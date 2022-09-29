function updateCount (body) {
  document.getElementById('count').innerText = body.amount
}

function handleClick (method) {
  apiRequest({ method })
    .then(updateCount)
}

async function apiRequest ({ method }) {
  const amount = document.getElementById('amount').value
  let options = {
    method,
    headers: {
      'Content-Type': 'application/json'
    }
  }
  if (method.toUpperCase() !== 'GET') {
    options.body = JSON.stringify({ amount })
  }

  try {
    const response = await fetch('/api/v1/counter', options)
    return await response.json()
  } catch (err) {
    console.error('api error', err)
    init()
  }
}

function init () {
  apiRequest({ method: 'GET' })
    .then(updateCount)
}

// run init!
init()
