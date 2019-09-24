var app = echarts.init(document.getElementById('yesterday_timer_graphy'));
app.title = '笛卡尔坐标系上的热力图';
var hours = ['8','9','10','11','12',
    '13','14','15','16','17','18','19','20','21','22','23'];
var days = ['周日', '周六', '周五',
        '周四', '周三', '周二', '周一'];
option = {
    tooltip: {
        position: 'top'
    },
    animation: false,
    grid: {
        height: '70%',
        y: '5%'
    },
    xAxis: {
        type: 'category',
        data: hours,
        splitArea: {
            show: true
        }
    },
    yAxis: {
        type: 'category',
        data: days,
        splitArea: {
            show: true
        }
    },
    visualMap: {
        min: 0,
        max: 60,
        calculable: true,
        orient: 'horizontal',
        left: 'center',
        bottom: '5%'
    },
    series: [{
        name: '计时（分钟）',
        type: 'heatmap',
        label: {
            normal: {
                show: true
            }
        },
        itemStyle: {
            emphasis: {
                shadowBlur: 10,
                shadowColor: 'rgba(0, 0, 0, 0.5)',
            },
        }
    }]
};
refrush()
function refrush() {
    $.post({
        url:'/HoursCome',
        dataType:'json',
        contentType:false,
        processData:false,
        success:function (redata) {
            var data = redata.week_map;
            data = data.map(function (item) {
                return [item[1], item[0], item[2] || '-'];
            });
            option['series'][0]['data']=data
            app.setOption(option);
        }
    })
}