//数字滚动
;(function($, window, document) {
    "use strict";
    var defaults = {
        deVal: 0,       //传入值
        className:'dataNums',   //样式名称
        digit:''    //默认显示几位数字
    };
    function rollNum(obj, options){
        this.obj = obj;
        this.options = $.extend(defaults, options);
        this.init = function(){
             this.initHtml(obj,defaults);
        }
    }
    rollNum.prototype = {
        initHtml: function(obj,options){
            console.log(obj,options.deVal)
            var nameDeVal = options.deVal.split('');
            var strHtml = '<ul class="' + options.className + ' inrow"><em class="dataIcon"></em>';
            var valLen = options.digit ||  (options.deVal + '').length;
            if(obj.find('.'+options.className).length <= 0){
                for(var i = 0; i<  valLen; i++){
                    if(nameDeVal[i]==","){
                        strHtml += '<li class="dataOne dataLine" style="width:30px;background:none;font-size:69px;"><div class="dataBoc"><div class="tt" t="38" style="font-family:\'微软雅黑\';"><em style="color:#fff5a1;font-family: "微软雅黑";" class="num0">,</em></div></div></li>';
                    }
                    if(nameDeVal[i]=="."){
                        strHtml += '<li class="dataOne dataLine" style="width:30px;background:none;font-size:69px;"><div class="dataBoc"><div class="tt" t="38" style="font-family:\'微软雅黑\';"><em style="color:#fff5a1;font-family: "微软雅黑";" class="num0">.</em></div></div></li>';
                    }
                    if(nameDeVal[i] !="," && nameDeVal[i] !="."){
                        strHtml += '<li class="dataOne "><div class="dataBoc"><div class="tt" t="38"><span class="num0">0</span> <span class="num1">1</span> <span class="num2">2</span> <span class="num3">3</span> <span class="num4">4</span><span class="num5">5</span> <span class="num6">6</span> <span class="num7">7</span> <span class="num8">8</span> <span class="num9">9</span><span class="num0">0</span> <span class="num1">1</span> <span class="num2">2</span> <span class="num3">3</span> <span class="num4">4</span><span class="num5">5</span> <span class="num6">6</span> <span class="num7">7</span> <span class="num8">8</span> <span class="num9">9</span><span class="num10">,</span><span class="num11">.</span></div></div></li>';
                    }
                }
                strHtml += '</ul>';
                obj.html(strHtml);
            }
              this.scroNum(obj, options);
        },
        scroNum: function(obj, options){
            var number = options.deVal;
			var $num_item = $(obj).find('.' + options.className).find('.tt');
            var h = $(obj).find('.dataBoc').height(); 
            $num_item.css('transition','all 1s ease-in-out');
            var numberStr = number.toString();
            if(numberStr.length <= $num_item.length - 1){
                var tempStr = '';
                for(var a = 0; a < $num_item.length - numberStr.length; a++){
                    tempStr += '0';
                }
                numberStr = tempStr + numberStr;
            }

            var numberArr = numberStr.split('');
            $num_item.each(function(i, item) {
                setTimeout(function(){
                    if(numberArr[i]==","){
                        $num_item.eq(i).html(",")
                        $num_item.eq(i).css({'font-size':'69px','background':'none','transition':'none','color':'#fff5a1','font-family': "微软雅黑"})
                    }
                    if(numberArr[i]=='.'){
                        $num_item.eq(i).html(".").css({'font-size':'69px','background':'none','transition':'none','color':'#fff5a1','font-family': "微软雅黑"})
                        // $num_item.eq(i)
                    }
                    if(numberArr[i] !="," && numberArr[i] !="."){
                        $num_item.eq(i).css('top',-parseInt(numberArr[i])*h - h*10 + 'px');
                    }
                },i*150)
            });
        }
    }
    $.fn.rollNum = function(options){
        var $that = this;
        var rollNumObj = new rollNum($that, options);
        rollNumObj.init();
    };
})(jQuery, window, document);