/**
 * Created by Gzp on 2016/10/14.
 */
KindEditor.ready(function(K) {
        K.create('textarea[name=story_description]',{
            resizeType : 1,
            allowPreviewEmoticons : false,
            <!--去掉远程上传的功能-->
            allowImageRemote : false,
            <!--后台处理上传图片的功url-->
            uploadJson : '/Game/uploadImg',
            items : [
                'source', '|', 'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', 'bold', 'italic', 'underline',
                'removeformat', '|', 'justifyleft', 'justifycenter', 'justifyright', 'insertorderedlist',
                'insertunorderedlist', '|', 'emoticons', 'image', 'link']

        });
        K.create('textarea[name=content]',{
            resizeType : 1,
            allowPreviewEmoticons : false,
            <!--去掉远程上传的功能-->
            allowImageRemote : false,
            <!--后台处理上传图片的功url-->
            uploadJson : '/Game/uploadImg/',
            items : [
                'source', '|', 'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', 'bold', 'italic', 'underline',
                'removeformat', '|', 'justifyleft', 'justifycenter', 'justifyright', 'insertorderedlist',
                'insertunorderedlist', '|', 'emoticons', 'image', 'link']

        });
        K.create('textarea[name=hint]',{
            resizeType : 1,
            allowPreviewEmoticons : false,
            <!--去掉远程上传的功能-->
            allowImageRemote : false,
            <!--后台处理上传图片的功url-->
            uploadJson : '/Game/uploadImg/',
            items : [
                'source', '|', 'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', 'bold', 'italic', 'underline',
                'removeformat', '|', 'justifyleft', 'justifycenter', 'justifyright', 'insertorderedlist',
                'insertunorderedlist', '|', 'emoticons', 'image', 'link']

        });
        K.create('textarea[name=game_description]',{
            resizeType : 1,
            allowPreviewEmoticons : false,
            <!--去掉远程上传的功能-->
            allowImageRemote : false,
            <!--后台处理上传图片的功url-->
            uploadJson : '/Game/uploadImg/',
            items : [
                'source', '|', 'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', 'bold', 'italic', 'underline',
                'removeformat', '|', 'justifyleft', 'justifycenter', 'justifyright', 'insertorderedlist',
                'insertunorderedlist', '|', 'emoticons', 'image', 'link']

        });
});