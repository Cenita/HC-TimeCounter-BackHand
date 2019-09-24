var secondTime = Number($(".secondNums").attr('value'));
var minuteTime = Number($(".minuetsNums").attr('value'));
var hoursTime = Number($(".hoursNums").attr('value'));
$(".hoursNums").rollNum({
        deVal:$(".hoursNums").attr('value')
    });
    console.log();
    $(".minuetsNums").rollNum({
        deVal:$(".minuetsNums").attr('value')
    });
    $(".secondNums").rollNum({
        deVal:$(".secondNums").attr('value')
    });
if($(".week_time").attr("isInTheRoom")=='Y'){
    window.setInterval(function () {
    secondTime+=1;
    if(secondTime==60){
        secondTime=0;
        minutesJinwei();
    }
    Refresh();
},1000);
}
function minutesJinwei() {
    minuteTime+=1;
    if(minuteTime==60){
        minuteTime=0;
        hoursTime+=1;
    }
}
function Refresh() {
    $(".hoursNums").rollNum({
        deVal:hoursTime.toString()
    });
    console.log();
    $(".minuetsNums").rollNum({
        deVal:minuteTime.toString()
    });
    $(".secondNums").rollNum({
        deVal:secondTime.toString()
    });
}