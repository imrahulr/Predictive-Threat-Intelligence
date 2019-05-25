import { Component, OnInit } from '@angular/core';
import { SessionService } from './service/session/session.service';
import { HttpErrorResponse } from '@angular/common/http';
import { ToastrService } from 'ngx-toastr';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  providers: [ SessionService ]
})

export class AppComponent implements OnInit {
  
  title = 'Threat Intelligence';
  isRequesting = false;
  sessionId = '';
  loaded = false;
  loadSeq = false;

  trueSeq = [];
  hmm = [];
  mc = [];
  lstm = [];

  constructor(
    public sessionService: SessionService,
    private toastr: ToastrService,
    private router: Router
  ) {}
  
  ngOnInit() {
    this.displayCommonIPs();
    this.displayCommonUsernames();
    this.displayCommonPasswords();
    this.displayCommonSystems();
    this.displayDestIPs();
  }

  getSession() {
    this.isRequesting = true;
    const req = { sessId: this.sessionId };
    this.sessionService.getSessionSeq(req).subscribe(
      data => {
        // console.log(data);
        this.loadSeq = false;
        this.loadSessionSeq(data['data']);
        this.isRequesting = false;
        this.loadSeq = true;
      },
      (err: HttpErrorResponse) => {
        this.isRequesting = false;
        this.toastr.error('Error retreiving session', 'Error');
        console.log('Error from getSession', err);
      }
    );
  }

  loadSessionSeq(data) {

    this.trueSeq = [];
    this.lstm = [];
    this.mc = [];
    this.hmm = [];

    this.trueSeq = data['true'];
    var temp = data['pred']
    
    this.lstm.push(17);
    this.mc.push(16);
    this.hmm.push(16);

    temp.forEach(element => {
      element = element['prediction'].replace(/\n|\r/g, "");
      element = element.replace(/'/g, '"');
      element = element.match(/\[(.*?)\]/g);
      this.lstm.push(JSON.parse(element[0])[0]);
      this.mc.push(JSON.parse(element[1])[0]);
      this.hmm.push(JSON.parse(element[2])[0]);
    });

    console.log(this.trueSeq);
    console.log(this.mc);
    console.log(this.hmm);
    console.log(this.lstm);

  }

  displayCommonIPs() {
    const req = { col: 'src_ip', max: 10 };
    this.sessionService.getValueCounts(req).subscribe(
      data => {
        data['data'].forEach(item => {
          this.IPBarChartLabels.push(item._id);
          this.IPBarChartData[0]['data'].push(item.count);
        });      
      },
      (err: HttpErrorResponse) => {
        this.toastr.error('Error retreiving data', 'Error');
        console.log('Error from getValueCounts', err);
      }
    ); 
  }
  public IPBarChartOptions = { 
    scaleShowVerticalLines: false,
    responsive: true,
    maintainAspectRatio: false, 
    scales: {
      xAxes: [{ scaleLabel: { display: true, labelString: 'No of Occurrences' }}],
      yAxes: [{ scaleLabel: { display: true, labelString: 'Source IP' }}]
    }     
  };
  public IPBarChartType = 'horizontalBar';
  public IPChartColors: any[] = [{ backgroundColor:"#FF7777"}];
  public barChartLegend = false;
  public IPBarChartLabels = [];
  public IPBarChartData = [{ data: [], label: 'Source IP'}];

  displayCommonUsernames() {
    const req = { col: 'username', max: 8 };
    this.sessionService.getValueCounts(req).subscribe(
      data => {
        data['data'].forEach(item => {
          this.UBarChartLabels.push(item._id);
          this.UBarChartData[0]['data'].push(item.count);
        });
      },
      (err: HttpErrorResponse) => {
        this.toastr.error('Error retreiving data', 'Error');
        console.log('Error from getValueCounts', err);
      }
    );
  }
  public UBarChartOptions = { 
    scaleShowVerticalLines: false,
    responsive: true,
    maintainAspectRatio: false, 
    scales: {
      xAxes: [{ scaleLabel: { display: true, labelString: 'Username' }}],
      yAxes: [{ scaleLabel: { display: true, labelString: 'No of Occurrences' }}]
    }     
  };
  public UBarChartType = 'bar';
  public UChartColors: any[] = [{ backgroundColor:"#77FF77"}];
  public UBarChartLabels = [];
  public UBarChartData = [{ data: [], label: 'Username'}];

  displayCommonPasswords() {
    const req = { col: 'password', max: 8 };
    this.sessionService.getValueCounts(req).subscribe(
      data => {
        data['data'].forEach(item => {
          this.PBarChartLabels.push(item._id);
          this.PBarChartData[0]['data'].push(item.count);
        });
      },
      (err: HttpErrorResponse) => {
        this.toastr.error('Error retreiving data', 'Error');
        console.log('Error from getValueCounts', err);
      }
    );
  }
  public PBarChartOptions  = { 
    scaleShowVerticalLines: false,
    responsive: true,
    maintainAspectRatio: false, 
    scales: {
      xAxes: [{ scaleLabel: { display: true, labelString: 'Password' }}],
      yAxes: [{ scaleLabel: { display: true, labelString: 'No of Occurrences' }}]
    }     
  };
  public PBarChartType = 'bar';
  public PChartColors: any[] = [{ backgroundColor:"#FFFF77"}];
  public PBarChartLabels = [];
  public PBarChartData = [{ data: [], label: 'Password'}];

  displayCommonSystems() {
    const req = { col: 'system', max: 5 };
    this.sessionService.getValueCounts(req).subscribe(
      data => {
        data['data'].forEach(item => {
          this.SDoughnutChartLabels.push(item._id);
          this.SDoughnutChartData.push(item.count);
          // this.loaded = true;
        });
      },
      (err: HttpErrorResponse) => {
        this.toastr.error('Error retreiving data', 'Error');
        console.log('Error from getValueCounts', err);
      }
    );
  }
  public SDoughnutChartLabels = [];
  public SDoughnutChartData = [];
  public SDChartOptions: any = {legend: { position: 'right' }, maintainAspectRatio: false}
  public SChartColors: any[] = [{ backgroundColor:["#FF7777", "#FFFF77", "#77FF77", "#7777FF", "#77FFFF"]}];
  public SDoughnutChartType = 'doughnut';

  displayDestIPs() {
    const req = { col: 'dst_ip', max: 4 };
    this.sessionService.getValueCounts(req).subscribe(
      data => {
        data['data'].forEach(item => {
          this.DBarChartLabels.push(item._id);
          this.DBarChartData[0]['data'].push(item.count);
          this.loaded = true;
        });      
      },
      (err: HttpErrorResponse) => {
        this.toastr.error('Error retreiving data', 'Error');
        console.log('Error from getValueCounts', err);
      }
    ); 
  }
  public DBarChartOptions = { 
    scaleShowVerticalLines: false,
    responsive: true,
    maintainAspectRatio: false, 
    scales: {
      xAxes: [{ scaleLabel: { display: true, labelString: 'Destination IP' }}],
      yAxes: [{ scaleLabel: { display: true, labelString: 'No of Occurrences' }}]
    }     
  };
  public DBarChartType = 'bar';
  public DChartColors: any[] = [{ backgroundColor:"#7777FF"}];
  public DBarChartLabels = [];
  public DBarChartData = [{ data: [], label: 'Destination IP'}];

  states = ['cowrie.client.size', 'cowrie.client.version', 'cowrie.command.failed', 
  'cowrie.command.input/delete', 'cowrie.command.input/dir_sudo', 'cowrie.command.input/other', 
  'cowrie.command.input/system', 'cowrie.command.input/write', 'cowrie.command.success', 
  'cowrie.direct-tcpip.data', 'cowrie.direct-tcpip.request', 'cowrie.log.closed', 
  'cowrie.log.open', 'cowrie.login.failed', 'cowrie.login.success', 'cowrie.session.closed', 
  'cowrie.session.connect', 'cowrie.session.file_download', 'cowrie.session.input']

}
