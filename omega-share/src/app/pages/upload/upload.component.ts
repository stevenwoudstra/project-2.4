import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { GlobalConstants } from 'src/app/global-constants';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.css']
})
export class UploadComponent implements OnInit {

  selectedFile: File | null = null;

  url : String = "";

  constructor(private http: HttpClient) { }
  
  ngOnInit(): void {
  }
  
  onFileSelected(event: any): void {

    
    document.getElementById("upload-icon")?.remove();
    let fileType = event.target!.files[0].name.split(".").pop().toUpperCase();
    let previewIcon: HTMLElement = document.getElementById("preview-icon")!;
    if(previewIcon.children[2]) previewIcon.children[2].remove();
    if(GlobalConstants.viewableFileTypes.includes(fileType)) {      
      previewIcon.firstElementChild!.setAttribute("src", "assets/icons/file_types/" + fileType + ".svg");
    } else {
      let typeLabel = document.createElement("label");
      typeLabel.innerHTML = "." + fileType;
      typeLabel.style.fontSize = ((3 / fileType.length) > 1 ? 1 : 3 / fileType.length) + "rem";
      typeLabel.style.transform = "translateY(-70px)";
      previewIcon.append(typeLabel);
      previewIcon.firstElementChild!.setAttribute("src", "assets/icons/file_types/unknown.svg");
    }
    var displayName = event.target!.files[0].name
    if(event.target!.files[0].name.length > 16) displayName = displayName.substring(0, 16) + "...";
    previewIcon.children[1].innerHTML = displayName;
    previewIcon.style.height = "100px";
    previewIcon.classList.toggle("fileAppear");
    previewIcon.classList.toggle("fileAppear2");

    // this.selectedFile = event.target.files[0];
    // const fd = new FormData();
    // fd.append('image', this.selectedFile!, this.selectedFile!.name);
    // this.http.post('omegashare.test', fd).subscribe(res => {
    //   console.log(res);
    // })


    // if(event.target.files) {
    //   let reader = new FileReader();
    //   reader.readAsDataURL(event.target.files[0]);
    //   reader.onload = (event:any) => {
    //     this.url = event.target.result;
    //   }
    // }

  }

}
