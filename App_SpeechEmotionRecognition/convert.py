{% extends 'base.html'%}
    {% block content%}
    {% if messages %}
        {% for message in messages %}
         {% if message.tags %}  <script>alert("{{ message }}")</script> {% endif %}

        {% endfor %}

    {% endif %}
<style>
input {
  border-top-style: hidden;
  border-right-style: hidden;
  border-left-style: hidden;
  border-bottom-style: hidden;
}

.no-outline:focus {
  outline: none;
}
</style>

<div style="background: url('/media/bg1.jpg'); background-repeat:no-repeat;background-size:cover;  height:650px; width: 100%;">
    <br>
    <h3 style="text-align: center;color: white;" ><mark style="color:blue;">Our Services</mark></h3>
    <br>
    <br>
<div class="modal" tabindex="-1" id = "myModal" >
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Speech Emotion Recognizer</h5>
        
      </div>
      <div class="modal-body">
        <p>You are in&nbsp;<input type="text" id="reply" class = "no-outline" name="reply" value=""></p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Done</button>
      </div>
    </div>
  </div>
</div>

 <div class="row">
    <div class = "container" style="width:50%;">
        <div class = "col-md-12">
            <div class="row">
                <div class="col-md-6" >
                    <img class="card-img-top "src="/media/audio.png" id ="imgFileUpload1"name="images"  style="height: 400px;width:100%;">
                    <span id="spnFilePath"></span>
                    <input type="file" id="imgupload" style="display:none"/> 
                    <!--<button id="OpenImgUpload">Image Upload</button>-->
                    <script type="text/javascript">
                        

                        {
                                    $.ajax({
                                        type: "POST",
                                        url: '{% url 'pred1' %}',
                                        data: 
                                        {    
                                            'id': 'first',
                                            
                                            'csrfmiddlewaretoken': '{{ csrf_token }}',
                                        },
                                        //dataType: 'json',
                                        success: function (data) 
                                        {
                                            var reply = data["respond"];
                                            document.getElementById("reply").value = reply;
                                            $('#myModal').modal('show');
                                            //alert(reply);
                                        }
                                    });
                                }
                       
                   
                    </script> 
                    <br>
                    <br>
                    <h3><p style="color:white;text-align:center;"> Choose an audio file</p></h3>   
                </div>
            
                <div class="col-md-6">
                    <img class="card-img-top "src="/media/record1.jpg" id ="imgFileUpload2"name="images" alt="Card image" style="height: 400px;width:100%;">
                    <script type="text/javascript">
                        $("img").click(function() {
                        //alert($(this).attr("id"));
                        //var No1 = $(this).attr("id");
                        {
                            $.ajax({
                                type: "POST",
                                url: '{% url 'RecordVoice' %}',
                                data: 
                                {
                                    
                                    'csrfmiddlewaretoken': '{{ csrf_token }}',
                                },
                                //dataType: 'json',
                                success: function (data) 
                                {
                                    var reply = data["respond"];
                                    document.getElementById("reply").value = reply;
                                    $('#myModal').modal('show');
                                }
                            });
                        }
                    });
                </script> 
                <br>
                <br>
                <h3><p style="color:white;text-align:center;h"> Use real-time audio</p></h3>
            </div>
        </div>
    </div>
</div>
</div>
</div>
<br>
{% endblock %}