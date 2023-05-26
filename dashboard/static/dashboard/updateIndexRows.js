$(document).ready(function() {
    setInterval(function() {
      var rows = document.querySelectorAll('.data-row');
      var row_ids = [];
      rows.forEach((row) => { var row_id = row.getAttribute('data-row-id'); row_ids.push(row_id);});
      function loopRows(row_ids){
          row_ids.forEach( row_id => {
              function getWord(status){
          switch(status){
              case 0:
                  return "good";
                  break;
              case 1:
                  return "okay";
                  break;
              case 2:
                  return "bad";
                  break;
              default:
                  return "unknown";
          }
          }
          $.ajax({
          url: 'check_dev_status/?row_id=' + row_id,  // URL to your Django view for checking dev_status updates
          method: 'GET',
          success: function(response) {
              $.each(response, function(index, row) {

                  // console.log("The row: " + JSON.stringify(row))
                  
                  var $devStatusElement = $('[data-row-id="' + row_id + '"]').find('.dev-status');
                  var $devCpuElement = $('[data-row-id="' + row_id + '"]').find('.dev-cpu');
                  var $devMemElement = $('[data-row-id="' + row_id + '"]').find('.dev-mem');
                  var $devHdElement = $('[data-row-id="' + row_id + '"]').find('.dev-hd');

                  var switch_status = getWord(row['dev_status'])

                  var devStatus = '<span class="' + switch_status + '"></span>'
                  var devCpu = String(row['dev_cpu']).trim()
                  var devMem = String(row['dev_mem']).trim()
                  var devHd = String(row['dev_hd']).trim()

                  if (devStatus !== $devStatusElement.html()) {
                      
                      $devStatusElement.html('<span class="' + switch_status + '"></span>');  // Update the content of the <td> element
                  }
                  if (devCpu !== $devCpuElement.text().trim()) {
                      console.log("row " + row['dev_cpu'])
                      console.log("cpu " + $devCpuElement.text())
                      $devCpuElement.html(`<span>${devCpu}</span>`);  // Update the content of the <td> element
                  }
                  if (devMem !== $devMemElement.text().trim()) {
                      console.log("row " + row['dev_mem'])
                      console.log("mem " + $devMemElement.text())
                      $devMemElement.html(`<span>${devMem}</span>`);  // Update the content of the <td> element
                  }
                  if (devHd !== $devHdElement.text().trim()) {
                      console.log("row " + row['dev_hd'])
                      console.log("hd " + $devHdElement.text())
                      $devHdElement.html(`<span>${devHd}</span>`);  // Update the content of the <td> element
                  }
              });
          },
          error: function(xhr, status, error) {
              console.error(error);
          }
          });

          });
          
      }
      loopRows(row_ids);
    }, 5000);  // Interval (in milliseconds) to check for updates (e.g., every 5 seconds)
  });