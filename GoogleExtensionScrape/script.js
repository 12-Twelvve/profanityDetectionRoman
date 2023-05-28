document.addEventListener('DOMContentLoaded', function () {
    var scrapeComment = document.getElementById('scrape');
    scrapeComment.addEventListener('click', scrape);
    var scrapeLiveComment = document.getElementById('scrape_live');
    scrapeLiveComment.addEventListener('click', scrape_live);
    function scrape(){
      chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        chrome.tabs.executeScript(tabs[0].id, {
          code: `var elements = document.querySelectorAll('yt-formatted-string#content-text.ytd-comment-renderer');
          innerHTMLs = [];
          for ( var i = 0; i < elements.length; ++i )
              innerHTMLs.push( elements[i].innerText );
          comments = innerHTMLs;
          title = document.querySelector('div#title > h1 >yt-formatted-string').innerText;
          chrome.runtime.sendMessage({ action: 'downloadData', title: title, comments: comments });
          `,
        });
      });}
      function scrape_live(){
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
          chrome.tabs.executeScript(tabs[0].id, {
            code: `
            var iframe = document.getElementById('chatframe');
            var iframeWindow = iframe.contentWindow;
            var elements = iframeWindow.document.querySelectorAll('yt-live-chat-text-message-renderer > div#content > span#message.yt-live-chat-text-message-renderer');
            innerHTMLs = [];
            console.log(elements.length)
            var innerHTMLs = Array.from(elements).map(function(element) {
                return element.innerText;
              });
            comments = innerHTMLs;
            title = document.querySelector('div#title > h1 >yt-formatted-string').innerText;
            chrome.runtime.sendMessage({ action: 'downloadData', title: title, comments: comments });
            `,
          });
        });}
    
  });

chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
if (message.action === 'downloadData') {
    var data = {
    title: message.title,
    comments: message.comments
    };
    var json = JSON.stringify(data, null, 2);
    var blob = new Blob([json], { type: 'application/json' });
    var downloadUrl = URL.createObjectURL(blob);
    var link = document.createElement('a');
    link.href = downloadUrl;
    link.download = message.title + '.json';
    link.click();
}
});