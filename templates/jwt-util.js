const fetchContent = (method, url) => new Promise((resolve, reject) => {
  const xhr = new window.XMLHttpRequest()
  const token = window.localStorage.getItem('iot14_tk')
  xhr.onreadystatechange = () => {
    if (xhr.readyState === window.XMLHttpRequest.DONE) {
      if (xhr.status === 200) resolve(xhr.responseText)
      else reject(new Error('fetchContent error'))
    }
  }
  xhr.open(method, url, true)
  xhr.setRequestHeader('Authorization', `Bearer ${token}`)
  xhr.send()
})
