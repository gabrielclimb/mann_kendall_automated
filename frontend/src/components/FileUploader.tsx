import React, { useCallback } from 'react'
import { useDropzone, DropzoneOptions } from 'react-dropzone'
import { Button } from '@/components/ui'

interface FileUploaderProps {
    onFileSelect: (file: File) => void
}

export const FileUploader: React.FC<FileUploaderProps> = ({ onFileSelect }) => {
    const onDrop = useCallback((acceptedFiles: File[]) => {
        if (acceptedFiles && acceptedFiles.length > 0) {
            onFileSelect(acceptedFiles[0])
        }
    }, [onFileSelect])

    const dropzoneOptions: DropzoneOptions = {
        onDrop,
        multiple: false,
        onDragEnter: () => { },
        onDragLeave: () => { },
        onDragOver: () => { }
    }

    const { getRootProps, getInputProps, isDragActive } = useDropzone(dropzoneOptions)

    return (
        <div {...getRootProps()} className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center cursor-pointer">
            <input {...getInputProps()} accept="text/csv,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" />
            {isDragActive ? (
                <p>Drop the file here ...</p>
            ) : (
                <p>Drag 'n' drop a file here, or click to select a file</p>
            )}
            <Button type="button" className="mt-4">Select File</Button>
        </div>
    )
}

