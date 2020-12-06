

    $(function() {
        function selectHTML() {
          var x = document.getElementsByTagName("u").hasAttribute("class");
            if (x == true){
              alert("no");
            }else{
          try {
              if (window.ActiveXObject) {
                  var c = document.selection.createRange();
                  return c.htmlText;
              }
          
              var nNd = document.createElement("u");
              var w = getSelection().getRangeAt(0);
              w.surroundContents(nNd);
              return nNd.innerHTML;
          } catch (e) {
              if (window.ActiveXObject) {
                  return document.selection.createRange();
              } else {
                  return getSelection();
              }
          }}
      }
          $('#labelpresperf').click( function() {
            
            var mytext = selectHTML();
              // $('span').wrap("<u class='presperf'></u>");
              $('u').css({"font-weight":"bold", "color":"blue"});
              $('u').attr({
                class:"present-perfect"
              });
          });

          $('#labelpastperf').click( function() {
              var mytext = selectHTML();
             // $('span').wrap("<u class='pastperf'></u>")
              $('u').css({"font-weight":"bold", "color":"pink"});
              $('u').attr({
                class:"past-perfect"
          });
          
          });

          $('#labelpresperfprogr').click( function() {
              var mytext = selectHTML();
              //$('span').wrap("<u class='presperfprogr'></u>")
              $('u').css({"font-weight":"bold", "color":"red"});
              $('u').attr({
                class:"present-perfect-progr"
          });
          
          });

          $('#labelpastperfprogr').click( function() {
              var mytext = selectHTML();
             // $('span').wrap("<u class='pastperfprogr'></u>")
              $('u').css({"font-weight":"bold", "color":"purple"});
              $('u').attr({
                class:"past-perfect-progr"
          });
          
          });

          $('#labelprogressive').click( function() {
              var mytext = selectHTML();
              //$('span').wrap("<u class='progressive'></u>")
              $('u').css({"font-weight":"bold", "color":"grey"});
              $('u').attr({
                class:"progressive"
          });
          
          });

          $('#labelconditional').click( function() {
              var mytext = selectHTML();
              //$('span').wrap("<u class='conditional'></u>")
              $('u').css({"font-weight":"bold", "color":"lightseagreen"});
              $('u').attr({
                class:"conditional"
          });
          
          });
          
          });

          $('#labelpassive').click( function() {
              var mytext = selectHTML();
              //$('span').wrap("<u class='passive'></u>")
              $('span').css({"font-weight":"bold", "color":"goldenrod"});
              $('span').attr({
                class:"passive"
          });
          
          });

          $('#btnespr').click( function() {
              var mytext = selectHTML();
             // $('span').wrap("<span class='idio'></span>")
              $('span').css({"font-weight":"bold", "color":"orangered"});
              $('span').attr({
                class:"idiomatic-epressions"
          });
          
          });

          $('#btnphr').click( function() {
              var mytext = selectHTML();
              //$('span').wrap("<mark class='highlight'></mark>")
              $('span').css({"font-weight":"bold", "background":"salmon"});
              $('span').attr({
                id:"phrasal-verbs"
          });
          
          });

          function surroundPresPerf() {
            var span = document.createElement("u");
                span.className = "present-perfect";
                
                if (window.getSelection) {
                    var sel = window.getSelection();
                    if (sel.rangeCount) {
                        var range = sel.getRangeAt(0).cloneRange();
                        range.surroundContents(span);
                        sel.removeAllRanges();
                        sel.addRange(range);
                    }
                }
            }
        
            function surroundPastPerf() {
                var span = document.createElement("u");
                span.className = "past-perfect";
                
                if (window.getSelection) {
                    var sel = window.getSelection();
                    if (sel.rangeCount) {
                        var range = sel.getRangeAt(0).cloneRange();
                        range.surroundContents(span);
                        sel.removeAllRanges();
                        sel.addRange(range);
                    }
                }
            }
        
            function surroundPresPerfProgr() {
            var span = document.createElement("u");
                span.className = "present-perfect-progr";
                
                if (window.getSelection) {
                    var sel = window.getSelection();
                    if (sel.rangeCount) {
                        var range = sel.getRangeAt(0).cloneRange();
                        range.surroundContents(span);
                        sel.removeAllRanges();
                        sel.addRange(range);
                    }
                }
            }
        
            function surroundPastPerfProgr() {
                var span = document.createElement("u");
                span.className = "past-perfect-progr";
                
                if (window.getSelection) {
                    var sel = window.getSelection();
                    if (sel.rangeCount) {
                        var range = sel.getRangeAt(0).cloneRange();
                        range.surroundContents(span);
                        sel.removeAllRanges();
                        sel.addRange(range);
                    }
                }
            }
        
            function surroundProgr() {
            var span = document.createElement("u");
                span.className = "progressive";
                
                if (window.getSelection) {
                    var sel = window.getSelection();
                    if (sel.rangeCount) {
                        var range = sel.getRangeAt(0).cloneRange();
                        range.surroundContents(span);
                        sel.removeAllRanges();
                        sel.addRange(range);
                    }
                }
            }
        
            function surroundCond() {
                var span = document.createElement("u");
                span.className = "conditional";
                
                if (window.getSelection) {
                    var sel = window.getSelection();
                    if (sel.rangeCount) {
                        var range = sel.getRangeAt(0).cloneRange();
                        range.surroundContents(span);
                        sel.removeAllRanges();
                        sel.addRange(range);
                    }
                }
            }
        
            function surroundFuture() {
            var span = document.createElement("u");
                span.className = "future";
                
                if (window.getSelection) {
                    var sel = window.getSelection();
                    if (sel.rangeCount) {
                        var range = sel.getRangeAt(0).cloneRange();
                        range.surroundContents(span);
                        sel.removeAllRanges();
                        sel.addRange(range);
                    }
                }
            }
        
            function surroundPassive() {
                var span = document.createElement("u");
                span.className = "passive";
                
                if (window.getSelection) {
                    var sel = window.getSelection();
                    if (sel.rangeCount) {
                        var range = sel.getRangeAt(0).cloneRange();
                        range.surroundContents(span);
                        sel.removeAllRanges();
                        sel.addRange(range);
                    }
                }
            }
        
            
        
            function surroundEspr() {
                var span = document.createElement("u");
                span.className = "idiomatic-epressions";
                
                if (window.getSelection) {
                    var sel = window.getSelection();
                    if (sel.rangeCount) {
                        var range = sel.getRangeAt(0).cloneRange();
                        range.surroundContents(span);
                        sel.removeAllRanges();
                        sel.addRange(range);
                    }
                }
            }
            function surroundPhr() {
                var span = document.createElement("u");
                span.className = "phrasal-verbs";
                
                if (window.getSelection) {
                    var sel = window.getSelection();
                    if (sel.rangeCount) {
                        var range = sel.getRangeAt(0).cloneRange();
                        range.surroundContents(span);
                        sel.removeAllRanges();
                        sel.addRange(range);
                    }
                }
            }