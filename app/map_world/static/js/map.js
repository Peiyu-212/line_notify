// 初始化 Datamap 地圖
// document.addEventListener('DOMContentLoaded', function winAnimation()
//     {
//         let winningSegmentNumber = spinner.getIndicatedSegmentNumber();
//         // Loop and set fillStyle of all segments to gray.
//         for (let x = 1; x < spinner.segments.length; x ++) {
//             spinner.segments[x].fillStyle = 'gray';
//         }

//         // Make the winning one yellow.
//         spinner.segments[winningSegmentNumber].fillStyle = 'pink';

//         // Call draw function to render changes.
//         spinner.draw();

//         // Also re-draw the pointer, otherwise it disappears.
//         drawColourTriangle();
//     }
// )
// // drawColourTriangle();

// // // Draw pointer on canvas, this time on the right.
// document.addEventListener('DOMContentLoaded', function drawColourTriangle()
//     {
//         // Get context used by the wheel
//         let ctx = spinner.ctx;
//         ctx.strokeStyle = 'navy';  // Set line colour.
//         ctx.fillStyle   = 'aqua';  // Set fill colour.
//         ctx.lineWidth   = 2;
//         ctx.beginPath();           // Begin path.

//         ctx.moveTo(420, 200);      // 調整指針位置
//         ctx.lineTo(370, 200);
//         ctx.lineTo(395, 175);
//         ctx.lineTo(420, 200);
//         ctx.stroke();              // Complete the path by stroking (draw lines).
//         ctx.fill();
//     }
// )

var map = new Datamap({
    element: document.getElementById('map'),
    height: 600,
    width: 1000,
    fills: {
    defaultFill: "#B7C731",
    activatedCountry: "#FFFACD",
    },
    geographyConfig: {
    popupOnHover: true,
    highlightOnHover: true
    }
});
  // 綁定地圖點擊事件
  const canvas = document.getElementById("choropleth_map");
  const { width, height } = canvas.getBoundingClientRect();
  const canvasFactor = width / height;
  selectedCountry = isoCodeConverter[Country[0].code];
  const countryFeature = map.current.svg.selectAll(`.datamaps-subunit.${selectedCountry}`)["0"]["0"].__data__;
  if (countryFeature !== undefined) {
    const bounds = path.bounds(countryFeature); // get bounds of selected country
    bounds.s = bounds[0][1];
    bounds.n = bounds[1][1];
    bounds.w = bounds[0][0];
    bounds.e = bounds[1][0];
    bounds.height = Math.abs(bounds.n - bounds.s);
    bounds.width = Math.abs(bounds.e - bounds.w);
    newScale = 0.95 / Math.max(bounds.width / width, bounds.height / height);
    const x = (bounds.w + bounds.e) / 2;
    const y = (bounds.s + bounds.n) / 2;

    /* specify the current zoom and translation vector */
    zoom.scale(newScale);
    zoom.translate([width / 2 - newScale * x, height / 2 - newScale * y]);

    /* dispatches a zoom gesture to registered listeners */
    zoom.event(map.current.svg.selectAll("g").transition().duration(2000));
    map.current.svg.selectAll("g").call(zoom);
  }
map.svg.selectAll('.datamaps-subunit').on('click', function(geo) {
    // 顯示模態視窗
    var modal = document.getElementById("myModal");
    var span = document.getElementsByClassName("close")[0];
    modal.style.display = 'block';
    
    // 從 Django API 獲取城市資料
    fetch('/map/get_cities_list/?nation=' + geo.properties.name)
    .then(response => {
        if (response.ok) {
        return response.json();
        } else {
        return Promise.reject(response.status);
        }
    }).then(data => {
        // 創建 spinner
        let spinner = new Winwheel({
            'canvasId': 'spinner',
            'numSegments': data.length,
            'segments': data.map(admin_city => ({text: admin_city})),
            // segmentColors: segmentColors,
            'fillStyle'      : '#F8F8FF',
            'rotationAngle'   : -30,
            'pointerAngle' : 90,
            'animation' :{
                'type'     : 'spinToStop',
                'duration' : 5,
                'spins'    : 8,
                // 'callbackFinished' : winAnimation,
                // 'callbackAfter' : drawColourTriangle
            }, 
            'pointerGuide' :        // Specify pointer guide properties.
            {
                'display'     : true,
                'strokeStyle' : 'red',
                'lineWidth'   : 3
            }
        });
        // 綁定轉盤停止事件
        spinner.stopAnimation(false);
        
        spinner.rotationAngle = 0;
        spinner.draw();
        spinner.startAnimation();
        setTimeout(() => {
        spinner.stopAnimation(true);
        }, 5000);
        // alert('Choose' + spinner.getIndicatedSegment().text)
    }).catch(error => {
        console.error('Fetch Error:', error);
    });
    span.onclick = function() {
        modal.style.display = "none";
    }
});

